import boto3
import json
import socket
import struct
import io
from pcapng import FileScanner

def ip_to_str(ip_bytes):
    """Convert IP bytes to a human-readable string."""
    return socket.inet_ntoa(ip_bytes)


def parse_tcp_header(tcp_segment): #TCP
    src_port, dst_port, seq, ack, offset_reserved_flags = struct.unpack('!HHLLH', tcp_segment[:14])
    offset = (offset_reserved_flags >> 12) * 4  # Data offset is in the top 4 bits
    return {
        'src_port': src_port,
        'dst_port': dst_port,
        'seq_num': seq,
        'ack_num': ack,
        'header_length': offset,
    }


def parse_udp_header(udp_segment):
    """Parse the UDP header."""
    src_port, dst_port, length, checksum = struct.unpack('!HHHH', udp_segment[:8])
    return {
        'src_port': src_port,
        'dst_port': dst_port,
        'length': length,
        'checksum': checksum,
    }


def read_pcapng(packets):
    # with open(file_path, 'rb') as fp:
    packet_info = []
    for block in packets:
        packet_info.clear()
        if hasattr(block, 'packet_data'):
            packet_data = block.packet_data
            
            # Parse Ethernet header
            eth_header = packet_data[:14]
            eth = struct.unpack('!6s6sH', eth_header)
            eth_protocol = socket.ntohs(eth[2])
            src_mac = ':'.join(format(x, '02x') for x in eth[0])
            dst_mac = ':'.join(format(x, '02x') for x in eth[1])

            # Parse IP header
            ip_header = packet_data[14:34]
            ip_fields = struct.unpack('!BBHHHBBH4s4s', ip_header)
            version_ihl = ip_fields[0]
            ihl = version_ihl & 0x0F  # Internet Header Length
            protocol = ip_fields[6]
            src_ip = ip_to_str(ip_fields[8])
            dst_ip = ip_to_str(ip_fields[9])
            total_length = ip_fields[2]
            header_length = ihl * 4

            # Default transport layer data
            transport_data = {
                "src_port": None,
                "dst_port": None,
                "extra_info": None,
            }

            # Parse transport layer protocol
            if protocol == 6:  # TCP
                tcp_segment = packet_data[14 + header_length:]
                tcp_info = parse_tcp_header(tcp_segment)
                transport_data.update(tcp_info)
            elif protocol == 17:  # UDP
                udp_segment = packet_data[14 + header_length:]
                udp_info = parse_udp_header(udp_segment)
                transport_data.update(udp_info)
            else:
                transport_data["extra_info"] = f"Unsupported Protocol: {protocol}"

            # Append the parsed data
            packet_info.append({
                "src_mac": src_mac,
                "dst_mac": dst_mac,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": protocol,
                "total_length": total_length,
                "header_length": header_length,
                "src_port": transport_data["src_port"],
                "dst_port": transport_data["dst_port"],
                "extra_info": transport_data.get("extra_info"),
            })

            # Send data to kinesis
            send_to_kinesis(packet_info_list=packet_info)


def send_to_kinesis(packet_info_list, stream_name='network-packets-streaming'):
    kinesis_client = boto3.client('kinesis')
    
    serialized_data = json.dumps(packet_info_list)  # Convert to JSON string
    
    # Send the serialized data to Kinesis
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=serialized_data.encode('utf-8'),  # Convert JSON string to bytes
            PartitionKey='partition-key' 
        )
        print(f"Successfully sent data to Kinesis: {response}")
    except Exception as e:
        print(f"Failed to send data to Kinesis: {e}")
        raise



def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            packets = FileScanner(io.BytesIO(response['Body'].read()))
            read_pcapng(packets=packets)    
            print(f"Successfully processed object: {object_key}")
            # s3_client.delete_object(Bucket=bucket_name, Key=object_key)

        except Exception as e:
            print(f"Error processing object: {object_key}, Error: {e}")
            # s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            raise e 

    return {
        'statusCode': 200,
        'body': json.dumps('S3 to Kinesis stream processing complete')
    }