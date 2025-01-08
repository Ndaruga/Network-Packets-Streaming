# Network-Packet-Streaming
Stream Network Packets from wireshark to kinesis

This guide explains how to set up Wireshark to capture network packets and save them as PCAPNG or PCAP files to a local directory every 1 second.

---
## Part 1: Set up Python to Listen for & Send PCAP to S3 - PCAP File Uploader

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
## Part 2: Configure Wireshark for realtime data packets streaming

This section explains how to configure Wireshark to save network packets as PCAPNG or PCAP files in a local directory every 1 second.

### Requirements
- Ensure you have appropriate permissions to capture network packets on your device.
- Capturing packets from certain networks may require administrative privileges or could be restricted based on organizational policies.

### Step 1: Download and Install Wireshark
- Download Wireshark from the official website: [Wireshark Download](https://www.wireshark.org/#downloadLink).
- Follow the installation instructions for your operating system.

### Step 2: Ensure NPCAP is Installed
- NPCAP is required for packet capturing. By default, NPCAP is *installed along with Wireshark*.
- If it is not installed, download it separately from [NPCAP Download](https://npcap.com/#download), and install it. If you have already launched wireshark, you might need to close and relaunch it.

### Step 3: Open Wireshark and Configure Capture Options
1. Launch Wireshark, select your interface (most likely Wi-Fi or Ethernet) and momentarily start and stop capturing packets

      ![image](https://github.com/user-attachments/assets/a01cfad7-741a-43b6-aca2-b5d22f695c6d)

      > Realize that wireshark has started capturing packets. Click on the **red stop button on the top left** to stop packets capture.

2. Click on **Capture** in the top menu.
3. From the dropdown menu, select **Options**.

      ![image](https://github.com/user-attachments/assets/864c4ad4-6618-46a2-ae47-077b0280955e)

> A  **Capture options** window pops up.

### Step 4: Configure Output Directory
1. In the poped up window, click **Output**.
2. In the **File** option, click **Browse** and select the `Saved-packets` directory created by the Python script ***(refer to Part 1 of the setup)***.
3. In the **File name** field, enter `packet` and click **Save**.
4. Check the box labeled **Create a new file automatically**.
5. In the options below, set the time interval for file creation to **1 second**. Ensure to Check the box labelled **after**.*(This interval can be adjusted as needed.)*

   ![image](https://github.com/user-attachments/assets/35ec7db9-3fd0-4f9f-9ae1-81744957be07)


### Step 5: Set Capture Duration
1. In the same pop-up, Select **Options**, then under **Stop capture automatically after**, set the duration to **5 minutes**.

   ![image](https://github.com/user-attachments/assets/10e48742-0842-425f-b6ff-855f210d5b24)


### Step 5: Start Capturing
- Click **Start** to begin capturing packets.
- Wireshark will now save network packets to the specified directory, creating a new file every 1 second.

  > **Note**: *Every time a file is created in the `Saved-packets` folder, it is uploaded to `S3` and instantly removed from the local folder*
---





## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

