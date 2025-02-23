# # import os
# # import re

# # def get_b_folders(base_dir):
# #     """ Get all folders in the form 'b<A>_<B>' sorted by <B> """
# #     folder_pattern = r"b\d+_(\d+)"  # Pattern to extract <B>
# #     b_folders = []

# #     for folder_name in os.listdir(base_dir):
# #         match = re.match(folder_pattern, folder_name)
# #         if match:
# #             b_value = int(match.group(1))  # Extract <B> value
# #             b_folders.append((folder_name, b_value))
    
# #     # Sort folders by <B> value
# #     return sorted(b_folders, key=lambda x: x[1])

# # def rename_files_in_folder(images_folder, labels_folder, start_c):
# #     """ Rename files in the 'images' and 'labels' folder starting from C=start_c, skipping existing files """
# #     current_c = start_c

# #     # Get all image and label files
# #     image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.png')])
# #     label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])

# #     for img_file, lbl_file in zip(image_files, label_files):
# #         while True:
# #             # Generate the new C value as a zero-padded 6-digit string
# #             new_c = f"{current_c:06d}"

# #             # Define new file names
# #             new_img_name = f"frame_{new_c}.png"
# #             new_lbl_name = f"frame_{new_c}.txt"

# #             # Full paths to old and new files
# #             old_img_path = os.path.join(images_folder, img_file)
# #             new_img_path = os.path.join(images_folder, new_img_name)

# #             old_lbl_path = os.path.join(labels_folder, lbl_file)
# #             new_lbl_path = os.path.join(labels_folder, new_lbl_name)

# #             # Check if the new file names already exist in any folder (globally unique)
# #             if os.path.exists(new_img_path) or os.path.exists(new_lbl_path):
# #                 print(f"Skipping C={new_c} as {new_img_name} or {new_lbl_name} already exists.")
# #                 current_c += 1  # Skip to the next number
# #             else:
# #                 # Rename image and label files
# #                 os.rename(old_img_path, new_img_path)
# #                 os.rename(old_lbl_path, new_lbl_path)
# #                 print(f"Renamed: {img_file} -> {new_img_name}")
# #                 print(f"Renamed: {lbl_file} -> {new_lbl_name}")

# #                 # Move to the next C value for the next file
# #                 current_c += 1
# #                 break

# #     return current_c

# # def rename_across_folders(base_dir):
# #     """ Main function to rename files across all 'b<A>_<B>' folders """
# #     b_folders = get_b_folders(base_dir)
# #     current_c = 1  # Start C from 1

# #     for folder_name, b_value in b_folders:
# #         print(f"Processing folder: {folder_name} (B={b_value})")

# #         # Define paths to the 'train/images' and 'train/labels' folders
# #         images_folder = os.path.join(base_dir, folder_name, "train", "images")
# #         labels_folder = os.path.join(base_dir, folder_name, "train", "labels")

# #         if os.path.exists(images_folder) and os.path.exists(labels_folder):
# #             # Rename files in this folder, starting with the current C value
# #             current_c = rename_files_in_folder(images_folder, labels_folder, current_c)
# #         else:
# #             print(f"Skipping folder {folder_name}: 'train/images' or 'train/labels' not found.")

# # # Example usage
# # base_directory = "C://Users//LAMBDA THETA//Downloads/batch5/train"  # Path to the base directory containing the 'b<A>_<B>' folders
# # rename_across_folders(base_directory)


# '''
# import os
# import re

# def get_b_folders(base_dir):
#     """ Get all folders in the form 'b<A>_<B>' sorted by <B> """
#     folder_pattern = r"b\d+_(\d+)"  # Pattern to extract <B>
#     b_folders = []

#     for folder_name in os.listdir(base_dir):
#         match = re.match(folder_pattern, folder_name)
#         if match:
#             b_value = int(match.group(1))  # Extract <B> value
#             b_folders.append((folder_name, b_value))
    
#     # Sort folders by <B> value
#     return sorted(b_folders, key=lambda x: x[1])

# def rename_files_in_folder(images_folder, labels_folder, start_c, output_images_folder, output_labels_folder):
#     """ 
#     #Rename copy files in 'images' and 'labels', and save them in separate output folders. 
#     Ensure filenames are unique by checking in the target folders.
#     """
#     current_c = start_c

#     # Get all image and label files
#     image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.png')])
#     label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])

#     for img_file, lbl_file in zip(image_files, label_files):
#         while True:
#             # Generate the new C value as a zero-padded 8-digit string
#             new_c = f"{current_c:08d}"

#             # Define new file names
#             new_img_name = f"frame_{new_c}.png"
#             new_lbl_name = f"frame_{new_c}.txt"

#             # Full paths to the new files in the output folders
#             new_img_path = os.path.join(output_images_folder, new_img_name)
#             new_lbl_path = os.path.join(output_labels_folder, new_lbl_name)

#             # Check if the new file names already exist in the output folders
#             if os.path.exists(new_img_path) or os.path.exists(new_lbl_path):
#                 print(f"Skipping C={new_c} as {new_img_name} or {new_lbl_name} already exists in output folders.")
#                 current_c += 1  # Skip to the next number
#             else:
#                 # Full paths to the old files
#                 old_img_path = os.path.join(images_folder, img_file)
#                 old_lbl_path = os.path.join(labels_folder, lbl_file)

#                 # Copy image and label files to the new folders with the new names
#                 os.rename(old_img_path, new_img_path)
#                 os.rename(old_lbl_path, new_lbl_path)

#                 print(f"Renamed and moved: {img_file} -> {new_img_name}")
#                 print(f"Renamed and moved: {lbl_file} -> {new_lbl_name}")

#                 # Move to the next C value for the next file
#                 current_c += 1
#                 break

#     return current_c

# def rename_across_folders(base_dir, output_images_folder, output_labels_folder):
#     """ 
#     Main function to rename files across all 'b<A>_<B>' folders and move them into 
#     separate output folders for images and labels.
#     """
#     b_folders = get_b_folders(base_dir)
#     current_c = 0  # Start C from 0 (as "frame_00000000")

#     # Ensure output directories exist
#     os.makedirs(output_images_folder, exist_ok=True)
#     os.makedirs(output_labels_folder, exist_ok=True)

#     for folder_name, b_value in b_folders:
#         print(f"Processing folder: {folder_name} (B={b_value})")

#         # Define paths to the 'train/images' and 'train/labels' folders
#         images_folder = os.path.join(base_dir, folder_name, "train", "images")
#         labels_folder = os.path.join(base_dir, folder_name, "train", "labels")

#         if os.path.exists(images_folder) and os.path.exists(labels_folder):
#             # Rename files in this folder, starting with the current C value
#             current_c = rename_files_in_folder(images_folder, labels_folder, current_c, output_images_folder, output_labels_folder)
#         else:
#             print(f"Skipping folder {folder_name}: 'train/images' or 'train/labels' not found.")

# # Example usage
# base_directory = "C://Users//LAMBDA THETA//Downloads/batch5/train"  # Path to the base directory containing the 'b<A>_<B>' folders
# rename_across_folders(base_directory)


'''
import os
import re

def get_b_folders(base_dir):
    """ Get all folders in the form 'b<A>_<B>' sorted by <B> """
    folder_pattern = r"b\d+_(\d+)"  # Pattern to extract <B>
    b_folders = []

    for folder_name in os.listdir(base_dir):
        match = re.match(folder_pattern, folder_name)
        if match:
            b_value = int(match.group(1))  # Extract <B> value
            b_folders.append((folder_name, b_value))
    
    # Sort folders by <B> value
    return sorted(b_folders, key=lambda x: x[1])

def rename_files_in_folder(images_folder, labels_folder, start_c, output_images_folder, output_labels_folder):
    """ 
    #Rename copy files in 'images' and 'labels', and save them in separate output folders. 
    Ensure filenames are unique by checking in the target folders.
    """
    current_c = start_c

    # Get all image and label files
    image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.png')])
    label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])

    for img_file, lbl_file in zip(image_files, label_files):
        while True:
            # Generate the new C value as a zero-padded 8-digit string
            new_c = f"{current_c:08d}"

            # Define new file names
            new_img_name = f"frame_{new_c}.png"
            new_lbl_name = f"frame_{new_c}.txt"

            # Full paths to the new files in the output folders
            new_img_path = os.path.join(output_images_folder, new_img_name)
            new_lbl_path = os.path.join(output_labels_folder, new_lbl_name)

            # Check if the new file names already exist in the output folders
            if os.path.exists(new_img_path) or os.path.exists(new_lbl_path):
                print(f"Skipping C={new_c} as {new_img_name} or {new_lbl_name} already exists in output folders.")
                current_c += 1  # Skip to the next number
            else:
                # Full paths to the old files
                old_img_path = os.path.join(images_folder, img_file)
                old_lbl_path = os.path.join(labels_folder, lbl_file)

                # Copy image and label files to the new folders with the new names
                os.rename(old_img_path, new_img_path)
                os.rename(old_lbl_path, new_lbl_path)

                print(f"Renamed and moved: {img_file} -> {new_img_name}")
                print(f"Renamed and moved: {lbl_file} -> {new_lbl_name}")

                # Move to the next C value for the next file
                current_c += 1
                break

    return current_c

def rename_across_folders(base_dir, output_images_folder, output_labels_folder):
    """ 
    Main function to rename files across all 'b<A>_<B>' folders and move them into 
    separate output folders for images and labels.
    """
    b_folders = get_b_folders(base_dir)
    current_c = 0  # Start C from 0 (as "frame_00000000")

    # Ensure output directories exist
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_labels_folder, exist_ok=True)

    for folder_name, b_value in b_folders:
        print(f"Processing folder: {folder_name} (B={b_value})")

        # Define paths to the 'train/images' and 'train/labels' folders
        images_folder = os.path.join(base_dir, folder_name, "train", "images")
        labels_folder = os.path.join(base_dir, folder_name, "train", "labels")

        if os.path.exists(images_folder) and os.path.exists(labels_folder):
            # Rename files in this folder, starting with the current C value
            current_c = rename_files_in_folder(images_folder, labels_folder, current_c, output_images_folder, output_labels_folder)
        else:
            print(f"Skipping folder {folder_name}: 'train/images' or 'train/labels' not found.")

# Example usage
base_directory = "C://Users//LAMBDA THETA//Downloads/batch5/train_n"        # Path to the base directory containing the 'b<A>_<B>' folders
output_images_folder = "C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/batch_5/train/images"     # Path to the output folder where renamed images will be saved
output_labels_folder = "C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/batch_5/train/labels"     # Path to the output folder where renamed labels will be saved

# # Rename and move files from all folders, starting from "frame_00000000"
# rename_across_folders(base_directory, output_images_folder, output_labels_folder)
# '''

import os
import re
import shutil

def get_b_folders(base_dir):
    """ Get all folders in the form 'b<A>_<B>' sorted by <B> """
    folder_pattern = r"b\d+_(\d+)"  # Pattern to extract <B>
    b_folders = []

    for folder_name in os.listdir(base_dir):
        match = re.match(folder_pattern, folder_name)
        if match:
            b_value = int(match.group(1))  # Extract <B> value
            b_folders.append((folder_name, b_value))
    
    # Sort folders by <B> value
    return sorted(b_folders, key=lambda x: x[1])

def copy_files_in_folder(images_folder, labels_folder, start_c, output_images_folder, output_labels_folder):
    """ 
    Copy files from 'images' and 'labels' folders, rename them in sequence, and save in separate output folders. 
    Ensure filenames are unique by checking in the target folders.
    """
    current_c = start_c

    # Get all image and label files
    image_files = sorted([f for f in os.listdir(images_folder) if (f.endswith('.PNG') or f.endswith('.png'))])
    label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])
    # print("image folder", images_folder)
    # print("image files", image_files)
    # print("labels folder", labels_folder)
    # print("labels file", label_files)

    for img_file, lbl_file in zip(image_files, label_files):
        while True:
            # Generate the new C value as a zero-padded 8-digit string
            new_c = f"{current_c:06d}"

            # Define new file names
            new_img_name = f"frame_{new_c}.png"
            new_lbl_name = f"frame_{new_c}.txt"

            # Full paths to the new files in the output folders
            new_img_path = os.path.join(output_images_folder, new_img_name)
            new_lbl_path = os.path.join(output_labels_folder, new_lbl_name)

            # Check if the new file names already exist in the output folders
            if os.path.exists(new_img_path) or os.path.exists(new_lbl_path):
                print(f"Skipping C={new_c} as {new_img_name} or {new_lbl_name} already exists in output folders.")
                current_c += 1  # Skip to the next number
            else:
                # Full paths to the old files
                old_img_path = os.path.join(images_folder, img_file)
                old_lbl_path = os.path.join(labels_folder, lbl_file)

                # Copy image and label files to the new folders with the new names
                shutil.copy2(old_img_path, new_img_path)
                shutil.copy2(old_lbl_path, new_lbl_path)

                # print(f"Copied and renamed: {img_file} -> {new_img_name}")
                # print(f"Copied and renamed: {lbl_file} -> {new_lbl_name}")

                # Move to the next C value for the next file
                current_c += 1
                break

    return current_c

def rename_across_folders(base_dir, output_images_folder, output_labels_folder):
    """ 
    Main function to copy and rename files across all 'b<A>_<B>' folders and save them into 
    separate output folders for images and labels.
    """
    b_folders = get_b_folders(base_dir)
    current_c = 0  # Start C from 0 (as "frame_00000000")

    # Ensure output directories exist
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_labels_folder, exist_ok=True)

    for folder_name, b_value in b_folders:
        print(f"Processing folder: {folder_name} (B={b_value})")

        # Define paths to the 'train/images' and 'train/labels' folders
        images_folder = os.path.join(base_dir, folder_name, "images", "train" )
        labels_folder = os.path.join(base_dir, folder_name, "labels", "train" )

        if os.path.exists(images_folder) and os.path.exists(labels_folder):
            # Copy and rename files in this folder, starting with the current C value
            current_c = copy_files_in_folder(images_folder, labels_folder, current_c, output_images_folder, output_labels_folder)
        else:
            print(f"Skipping folder {folder_name}: 'images/train' or 'labels/train' not found.")

# Example usage
base_directory = "D:/Wajahat/keypoints"#"C:/Users/LAMBDA THETA/Downloads/remain"        # Path to the base directory containing the 'b<A>_<B>' folders
output_images_folder = "C:/OsamaEjaz/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/updated_dataset/train/images"     # Path to the output folder where copied images will be saved
output_labels_folder = "C:/OsamaEjaz/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/updated_dataset/train/labels"#"C:/OsamaEjaz/Qiyas_Gaze_Estimation/Wajahat_Yolo_keypoint/updated_dataset/train/labels"     # Path to the output folder where copied labels will be saved

# Copy and rename files from all folders, starting from "frame_00000000"
rename_across_folders(base_directory, output_images_folder, output_labels_folder)
