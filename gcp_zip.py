import os
import zipfile
import re
import paramiko
from collections import deque

# SSH and SFTP parameters
hostname = '35.223.95.78'  # Replace with your instance's IP address
port = 22  # Default SSH port
username = 'haithem-ge'  # Replace with your SSH username
private_key_path = 'C:/Users/LAMBDA THETA/Downloads/haithem-ge-v100 (1)'  # Replace with your private key path

# Define the source directory containing the images
source_folder = "C:/Users/LAMBDA THETA/Downloads/remain/b8_15/images/train"  # Replace with your folder path

# Define the destination directory for the ZIP files locally
local_zip_folder = "C:/Users/LAMBDA THETA/Downloads/zipped_batches"  # Replace with your desired save path

# Define the remote directory for the ZIP files
remote_directory = 'wajahat/pose/zip'  # Update to your desired remote directory

# Ensure the local ZIP directory exists
os.makedirs(local_zip_folder, exist_ok=True)

# Supported image extensions
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

# List all files in the source directory
all_files = os.listdir(source_folder)

# Filter out image files matching the 'frame_######' pattern
image_files = [f for f in all_files if re.match(r'frame_\d{6}', f) and os.path.splitext(f)[1].lower() in image_extensions]

# Sort images numerically based on the number in the filename
image_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Initialize SSH transport
key = paramiko.RSAKey.from_private_key_file(private_key_path)
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, pkey=key)

# Initialize SFTP client
sftp = paramiko.SFTPClient.from_transport(transport)

# Deque to keep track of uploaded files
# uploaded_files = deque(maxlen=3)
# upload_counter = 0
created_zip_files = []

batch_size = 50
for i in range(0, len(image_files), batch_size):
    # Select the current batch of images
    batch_files = image_files[i:i + batch_size]
    
    # Determine the ZIP file name based on the first image's number in the batch
    first_image_number = int(re.search(r'\d+', batch_files[0]).group())
    zip_filename = f'frame_{first_image_number}.zip'
    zip_filepath = os.path.join(local_zip_folder, zip_filename)
    
    # Create the ZIP file and add the selected images
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for image in batch_files:
            image_path = os.path.join(source_folder, image)
            zipf.write(image_path, arcname=image)
    
    print(f'Created {zip_filepath} containing {len(batch_files)} images.')

    created_zip_files.append(zip_filepath)
    
    # Define the remote path for the ZIP file
    remote_path = os.path.join(remote_directory, zip_filename).replace("\\", "/")
    
    # Create remote directory if it doesn't exist
    remote_dir = os.path.dirname(remote_path)
    try:
        sftp.stat(remote_dir)
    except FileNotFoundError:
        sftp.mkdir(remote_dir)
    
    # Upload the ZIP file
    sftp.put(zip_filepath, remote_path)
    print(f'Uploaded {zip_filepath} to {remote_path}')
    
    # Add the uploaded file to the deque
    # uploaded_files.append(remote_path)
    # upload_counter +=1
    
    # # If three files have been uploaded, delete the oldest one
    # if upload_counter % 3 == 0:
    #     try:
    #         os.remove(zip_filepath)
    #         print(f'Deleted local file {zip_filepath}')
    #     except OSError as e:
    #         print(f'Error deleting file {zip_filepath}: {e}')

    if len(created_zip_files) > 2:
        file_to_delete = created_zip_files.pop(0)
        try:
            os.remove(file_to_delete)
            print(f'Deleted local file {file_to_delete}')
        except OSError as e:
            print(f'Error deleting file {file_to_delete}: {e}')

# Close SFTP and SSH connections
sftp.close()
transport.close()
