import os
import re
import shutil
import zipfile

def get_b_folders(base_dir):
    """ Get all folders in the form 'b<A>_<B>' sorted by <B> """
    folder_pattern = r"b\d+_(\d+)"  # Pattern to extract <B>
    b_folders = []

    for folder_name in os.listdir(base_dir):
        match = re.match(folder_pattern, folder_name, re.IGNORECASE)
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
    image_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith('.png') or f.lower().endswith('.PNG')])
    label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])

    for img_file, lbl_file in zip(image_files, label_files):
        while True:
            # Generate the new C value as a zero-padded 6-digit string
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

                print(f"Copied and renamed: {img_file} -> {new_img_name}")
                print(f"Copied and renamed: {lbl_file} -> {new_lbl_name}")

                # Move to the next C value for the next file
                current_c += 1
                break

    return current_c

def process_zip_files(zip_folder_path, output_images_folder, output_labels_folder):
    """
    Process each ZIP file in the given folder: unzip into a folder named after the ZIP file (without extension),
    rename frames and labels, and clean up.
    """
    current_c = 0  # Start C from 0 (as "frame_000000")

    # Ensure output directories exist
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_labels_folder, exist_ok=True)

    # Iterate over each file in the zip_folder_path
    for zip_filename in sorted(os.listdir(zip_folder_path)):
        if zip_filename.lower().endswith('.zip'):
            zip_path = os.path.join(zip_folder_path, zip_filename)
            zip_name = os.path.splitext(zip_filename)[0]  # Extract the base name of the ZIP file
            print(f"Processing ZIP file: {zip_filename}")

            # Create a directory named after the ZIP file (without extension)
            extract_dir = os.path.join(zip_folder_path, zip_name)
            os.makedirs(extract_dir, exist_ok=True)

            # Extract ZIP file into the newly created directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # Process the extracted contents
            b_folders = get_b_folders(extract_dir)
            for folder_name, b_value in b_folders:
                print(f"Processing folder: {folder_name} (B={b_value})")

                # Define paths to the 'train/images' and 'train/labels' folders
                images_folder = os.path.join(extract_dir, folder_name, "images", "train")
                labels_folder = os.path.join(extract_dir, folder_name, "labels", "train")

                if os.path.exists(images_folder) and os.path.exists(labels_folder):
                    # Copy and rename files in this folder, starting with the current C value
                    current_c = copy_files_in_folder(images_folder, labels_folder, current_c, output_images_folder, output_labels_folder)
                    print(f"copying image {current_c}")
                else:
                    print(f"Skipping folder {folder_name}: 'images/train' or 'labels/train' not found.")

            # Clean up: remove the extracted directory after processing
            shutil.rmtree(extract_dir)
            print(f"Cleaned up extracted directory: {extract_dir}")

# Example usage
zip_folder_path = "C:/Users/LAMBDA THETA/Downloads/remain"#"D:/Wajahat/keypoints"  # Path to the folder containing ZIP files
output_images_folder = "C:/wajahat/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/zip/train/images"  # Path to the output folder for images
output_labels_folder = "C:/wajahat/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/zip/train/labels"  # Path to the output folder for labels

# Process and rename files from all ZIP files
process_zip_files(zip_folder_path, output_images_folder, output_labels_folder)
