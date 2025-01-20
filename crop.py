# crop images script 
from PIL import Image
import os

def crop_selected_folders(parent_folder, selected_folders, output_parent_folder):
    """
    Crop images from specific subfolders inside the parent folder and save into structured output folders.
    Handles duplicate filenames by appending folder names to output filenames.

    Args:
        parent_folder (str): Path to the parent folder containing subfolders.
        selected_folders (list): List of folder names to process.
        output_parent_folder (str): Path to the parent folder where cropped images will be saved.
    """
    # Ensure output parent folder exists
    os.makedirs(output_parent_folder, exist_ok=True)

    # Crop ranges: (left, upper, right, lower)
    crop_ranges = [
        (60, 0, 370, None),   # First crop
        (370, 0, 730, None),  # Second crop
        (730, 0, 1080, None), # Third crop
        (1080, 0, None, None) # Fourth crop (till end)
    ]

    # Process only selected folders
    for folder_name in selected_folders:
        folder_path = os.path.join(parent_folder, folder_name)
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_name}' does not exist. Skipping...")
            continue

        print(f"Processing folder: {folder_name}")
        output_folder = os.path.join(output_parent_folder, folder_name)
        os.makedirs(output_folder, exist_ok=True)

        # Process images inside the folder
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                input_file_path = os.path.join(folder_path, file_name)
                img = Image.open(input_file_path)

                # Crop the image and save
                for i, (left, upper, right, lower) in enumerate(crop_ranges, start=1):
                    right = right if right else img.width
                    lower = lower if lower else img.height

                    cropped_img = img.crop((left, upper, right, lower))

                    # Create unique output filename
                    cropped_file_name = f"{folder_name}_{os.path.splitext(file_name)[0]}_crop{i}.jpg"
                    cropped_img.save(os.path.join(output_folder, cropped_file_name))

    print("Cropping complete. Images saved in:", output_parent_folder)


# Example usage
parent_folder = r"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/frames_output"  # Replace with your parent folder
selected_folders = ["v1", "v2", "v3","v4","v5","v6","v7","v8","v9","v10","v11","v12","v13","v14","v15","v16","v17","v18","v19","v20","v21","v22","v23","v24","v25","v26","v27","v28","v29"]  # List of folders to process
output_parent_folder = r"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/frames_output/cropped_output"  # Output folder path

# crop_selected_folders(parent_folder, selected_folders, output_parent_folder)

####################################################################################
# crop images sorting 
import os
import shutil
import re

def move_range_of_images(source_folder, destination_folder, file_prefix, start_index, end_index, file_suffix):
    """
    Move a range of image files from the source folder to the destination folder.

    Args:
        source_folder (str): Path to the folder containing the files.
        destination_folder (str): Path to the folder where files will be moved.
        file_prefix (str): Prefix of the file name (e.g., "v1_frame_").
        start_index (int): Starting index of the file range (inclusive).
        end_index (int): Ending index of the file range (inclusive).
        file_suffix (str): Suffix of the file name (e.g., "_crop2.jpg").
    """
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Compile a regex pattern to match filenames in the desired range
    pattern = re.compile(rf"{file_prefix}(\d+){file_suffix}$")

    # Loop through files in the source folder
    for file_name in os.listdir(source_folder):
        match = pattern.match(file_name)
        if match:
            file_index = int(match.group(1))
            if start_index <= file_index <= end_index:
                # Construct full paths
                source_file_path = os.path.join(source_folder, file_name)
                destination_file_path = os.path.join(destination_folder, file_name)
                
                # Move the file
                shutil.move(source_file_path, destination_file_path)
                print(f"Moved: {file_name}")

    print("File moving complete.")

# Example usage
source_folder = r"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/frames_output/cropped_output/v27"  # Source folder
destination_folder = r"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/frames_output/handraise"  # Destination folder
file_prefix = "v27_frame_"  # Common prefix of the files
start_index = 122  # Starting file index
end_index = 167  # Ending file index
file_suffix = "_crop1.jpg"  # Suffix of the files to move

# move_range_of_images(source_folder, destination_folder, file_prefix, start_index, end_index, file_suffix)

##############################################################################
# script for non handraise 

import os
import shutil

def move_pictures_to_single_folder(parent_folder, selected_folders, destination_folder):

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Initialize a set to keep track of existing filenames
    existing_files = set(os.listdir(destination_folder))

    # Process each selected folder
    for folder_name in selected_folders:
        folder_path = os.path.join(parent_folder, folder_name)

        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_name}' does not exist. Skipping...")
            continue

        print(f"Processing folder: {folder_name}")
        
        # Iterate through files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.jpg', '.png', '.jpeg')):  # Process only image files
                source_file_path = os.path.join(folder_path, file_name)
                
                # Ensure unique filenames in the destination folder
                base_name, ext = os.path.splitext(file_name)
                new_file_name = file_name
                counter = 1
                while new_file_name in existing_files:
                    new_file_name = f"{base_name}_{counter}{ext}"
                    counter += 1
                
                # Move the file
                destination_file_path = os.path.join(destination_folder, new_file_name)
                shutil.move(source_file_path, destination_file_path)
                existing_files.add(new_file_name)  # Update the set of existing files

                print(f"Moved: {file_name} --> {new_file_name}")

    print("File moving complete. All pictures are in:", destination_folder)


# Example usage
parent_folder = r"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/frames_output/cropped_output"  # Parent folder path
# selected_folders = ["v1", "v2", "v3"]  # List of folder names to process
selected_folders = ["v1", "v2", "v3","v4","v5","v7","v8","v9","v10","v11","v12","v13","v14","v15","v16","v18","v19","v20","v21","v22","v23","v24","v25","v26","v27"]  # List of folders to process
destination_folder = r"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/frames_output/Not_handraise"  # Destination folder path

move_pictures_to_single_folder(parent_folder, selected_folders, destination_folder)
