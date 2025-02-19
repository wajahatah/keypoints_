# import paramiko
# import os

# private_key_path = "C:/Users/LAMBDA THETA/Downloads/odc_v100_deploy.txt"
# local_path = "C:/OsamaEjaz/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/updated_dataset/train/images/frame_000000.png"
# remote_path = "/wajahat/pose/train/images"
# hostname = '35.223.95.78'
# username = "haithem-ge"

# key = paramiko.RSAKey.from_private_key_file(private_key_path)
# transport = paramiko.Transport((hostname, 22))
# transport.connect(username=username, pkey=key)
# sftp = paramiko.SFTPClient.from_transport(transport)

# for root, dirs, files in os.walk(local_path):
#     for file in files:
#         local_file = os.path.join(root, file)
#         relative_path = os.path.relpath(local_file, local_path)
#         remote_file = os.path.join(remote_path, relative_path)
#         remote_dir = os.path.dirname(remote_file)
#         try:
#             sftp.stat(remote_dir)
#         except FileNotFoundError:
#             sftp.mkdir(remote_dir)
#         sftp.put(local_file, remote_file)

# sftp.close()
# transport.close()


import paramiko
import os
from pathlib import PurePosixPath

# SSH and SFTP parameters
hostname = '35.223.95.78'  # Replace with your instance's IP address
port = 22  # Default SSH port
username = 'haithem-ge'  # Replace with your SSH username
private_key_path = 'C:/Users/LAMBDA THETA/Downloads/haithem-ge-v100 (1)'  # Replace with the path to your private key
local_directory = "C:/OsamaEjaz/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/updated_dataset/val/images"  # Replace with your local directory path
remote_directory = 'wajahat/pose/val/images'  # Replace with your remote directory path

# Initialize SSH transport
key = paramiko.RSAKey.from_private_key_file(private_key_path)
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, pkey=key)

# Initialize SFTP client
sftp = paramiko.SFTPClient.from_transport(transport)

# Iterate over files in the local directory
for root, _, files in os.walk(local_directory):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, local_directory)
        remote_path = os.path.join(remote_directory, relative_path).replace("\\", "/")

        # Create remote directory if it doesn't exist
        # remote_dir = os.path.dirname(remote_path)
        # try:
            # sftp.stat(remote_dir)
        # except FileNotFoundError:
            # sftp.mkdir(remote_dir)

        # Upload file
        sftp.put(local_path, remote_path)
        print(f'Uploaded {local_path} to {remote_path}')

# Close SFTP and SSH connections
sftp.close()
transport.close()
