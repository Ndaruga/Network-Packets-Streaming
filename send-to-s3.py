import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configuration
S3_BUCKET_NAME = 'network-packets-streaming'
PCAP_DIRECTORY = r'Saved-packets'

def upload_files_to_s3(directory):
    s3_client = boto3.client('s3')

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            s3_client.upload_file(file_path, S3_BUCKET_NAME, f'{PCAP_DIRECTORY}/{filename}')
            os.remove(file_path)
            print(f'Successfully uploaded {filename} to {S3_BUCKET_NAME} ✅')
        except FileNotFoundError:
            print(f'The file {filename} was not found. ❌')
        except NoCredentialsError:
            print('Credentials not available. ❌')
        except PartialCredentialsError:
            print('Incomplete credentials provided. ❌')
        except Exception as e:
            print(f'An error occurred: {e} ❌')

if __name__ == "__main__":
    upload_files_to_s3(PCAP_DIRECTORY)
