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

def rename_files_in_folder(images_folder, labels_folder, start_c):
    """ Rename files in the 'images' and 'labels' folder starting from C=start_c """
    current_c = start_c

    # Get all image and label files
    image_files = sorted([f for f in os.listdir(images_folder) if (f.endswith('.PNG') or f.endswith('.png'))])
    label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])
    print("File List:",image_files)
    for img_file, lbl_file in zip(image_files, label_files):
        # Generate the new C value as a zero-padded 6-digit string
        new_c = f"{current_c:05d}"

        # Define new file names
        new_img_name = f"frame_{new_c}.png"
        new_lbl_name = f"frame_{new_c}.txt"

        # Full paths to old and new files
        old_img_path = os.path.join(images_folder, img_file)
        new_img_path = os.path.join(images_folder, new_img_name)

        old_lbl_path = os.path.join(labels_folder, lbl_file)
        new_lbl_path = os.path.join(labels_folder, new_lbl_name)

        if os.path.exists(new_img_path) or os.path.exists(new_lbl_path):
                print(f"Skipping C={new_c} as {new_img_name} or {new_lbl_name} already exists.")
                current_c += 1  # Skip to the next number
        # Rename image and label files
        else:
            os.rename(old_img_path, new_img_path)
            os.rename(old_lbl_path, new_lbl_path)

        print(f"Renamed: {img_file} -> {new_img_name}")
        print(f"Renamed: {lbl_file} -> {new_lbl_name}")

        # Increment the current C value
        current_c += 1

    return current_c

def rename_across_folders(base_dir):
    """ Main function to rename files across all 'b<A>_<B>' folders """
    b_folders = get_b_folders(base_dir)
    current_c = 0  # Start C from 0

    for folder_name, b_value in b_folders:
        print(f"Processing folder: {folder_name} (B={b_value})")

        # Define paths to the 'train/images' and 'train/labels' folders
        images_folder = os.path.join(base_dir, folder_name, "train", "images")
        labels_folder = os.path.join(base_dir, folder_name, "train", "labels")

        if os.path.exists(images_folder) and os.path.exists(labels_folder):
            # Rename files in this folder, starting with the current C value
            current_c = rename_files_in_folder(images_folder, labels_folder, current_c)
        else:
            print(f"Skipping folder {folder_name}: 'train/images' or 'train/labels' not found.")

# Example usage
base_directory = "C://Users//LAMBDA THETA//Downloads/batch5/train"  # Path to the base directory containing the 'b<A>_<B>' folders
rename_across_folders(base_directory)
