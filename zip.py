import os
import zipfile
import re

# Define the source directory containing the images
source_folder = "C:/Users/LAMBDA THETA/Downloads/remain/b8_15/images/train"  # Replace with your folder path

# Define the destination directory for the ZIP files
destination_folder = "C:/Users/LAMBDA THETA/Downloads"  # Replace with your desired save path

# Ensure the destination directory exists
os.makedirs(destination_folder, exist_ok=True)

# Supported image extensions
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

# List all files in the source directory
all_files = os.listdir(source_folder)

# Filter out image files matching the 'frame_######' pattern
image_files = [f for f in all_files if re.match(r'frame_\d{6}', f) and os.path.splitext(f)[1].lower() in image_extensions]

# Sort images numerically based on the number in the filename
image_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

batch_size = 100
for i in range(0, len(image_files), batch_size):
    # Select the current batch of images
    batch_files = image_files[i:i + batch_size]
    
    # Determine the ZIP file name based on the first image's number in the batch
    first_image_number = int(re.search(r'\d+', batch_files[0]).group())
    zip_filename = f'frame_{first_image_number}.zip'
    zip_filepath = os.path.join(destination_folder, zip_filename)
    
    # Create the ZIP file and add the selected images
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for image in batch_files:
            image_path = os.path.join(source_folder, image)
            zipf.write(image_path, arcname=image)
    
    print(f'Created {zip_filepath} containing {len(batch_files)} images.')
    
# # Select the first 100 images
# images_to_zip = image_files[:100]

# # Determine the ZIP file name based on the first image's number
# if images_to_zip:
#     first_image_number = int(re.search(r'\d+', images_to_zip[0]).group())
#     zip_filename = f'frame_{first_image_number}.zip'
#     zip_filepath = os.path.join(destination_folder, zip_filename)
# else:
#     print("No images found to zip.")
#     exit()

# # Create the ZIP file and add the selected images
# with zipfile.ZipFile(zip_filepath, 'w') as zipf:
#     for image in images_to_zip:
#         image_path = os.path.join(source_folder, image)
#         zipf.write(image_path, arcname=image)

# print(f'Created {zip_filepath} containing {len(images_to_zip)} images.')
