# Network-Packet-Streaming
Stream Network Packets from wireshark to kinesis


---
## Part 1: Set up python to listen for & Send PCAP to S3 - PCAP File Uploader

This Python script monitors a specified directory for new PCAP files and uploads them to an Amazon S3 bucket. If a file is found, it uploads the file and removes it from the local directory.

### Requirements

Before running the script, ensure you have the following:

- **Python 3.x**: Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- **Boto3 Library**: This is the AWS SDK for Python, which allows you to interact with Amazon S3. You can install it using pip.
- **IAM Permissions**: Ensure that your AWS IAM user has permissions to upload files to the specified S3 bucket.

### Installation and Running

1. Clone or [Download](https://github.com/Ndaruga/Network-Packets-Streaming/archive/refs/heads/main.zip) the Repository

   ```bash
   git clone https://github.com/Ndaruga/Network-Packets-Streaming.git
   ```

2. Navigate into the cloned directory
   
   ```bash
   cd Network-Packets-Streaming
   ```

   *You can create a virtual environment (Optional)*
   
3. **Install the requirements**:
   Run the following command to install the necessary requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. **AWS Credentials**:
   Ensure you have your AWS credentials set up. You can configure them in the `~/.aws/credentials` file or set them as environment variables. The credentials file should look like this:

   ```
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY_ID
   aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
   ```

5. **Run the script using Python**:

   ```bash
   python send-to-s3.py
   ```

6. The script will **start monitoring** the `Saved-packets` directory for new PCAP files every second. If a new file is found, it will upload it to the specified S3 bucket (`network-packets-streaming`) and remove it from the local directory.

   ***The script will run indefinitely until manually terminated (e.g., by pressing `Ctrl + C`).***


---
## Part 2: Configure Wireshark


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

