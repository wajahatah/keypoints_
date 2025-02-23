import os
import zipfile
import re
import shutil

def unzip_files_in_folder(folder_path, unzip_folder):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    for file in os.listdir(folder_path):
        if file.endswith(".zip"):
            # zip_path = os.path.join(folder_path, file)
            folder_name = os.path.splitext(file)[0]
            # extract_path = os.path.join(folder_path, folder_name) #to save unzip files in same folder
            extract_path = os.path.join(unzip_folder, folder_name)

            if os.path.exists(extract_path):
                print(f"Skipping '{file}': Already extracted in '{extract_path}'")
                continue

            os.makedirs(extract_path, exist_ok=True)
            
            # with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # with zipfile.ZipFile((folder_path,file), 'r') as zip_ref:
            with zipfile.ZipFile(os.path.join(folder_path, file), 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                print(f"Extracted '{file}' to '{extract_path}'")

def get_b_folders(base_dir):
    folder_pattern = r"b\d+_(\d+)"
    b_folders = []
    
    for folder_name in os.listdir(base_dir):
        match = re.match(folder_pattern, folder_name, re.IGNORECASE)
        if match:
            b_value = int(match.group(1))
            b_folders.append((folder_name, b_value))
    
    return sorted(b_folders, key=lambda x: x[1])

def move_files_in_folder(images_folder, labels_folder, start_c, output_images_folder, output_labels_folder):
    current_c = start_c
    image_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith('.png') or f.lower().endswith('.PNG')])
    label_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])
    
    for img_file, lbl_file in zip(image_files, label_files):
        while True:
            new_c = f"{current_c:06d}"
            new_img_name = f"frame_{new_c}.png"
            new_lbl_name = f"frame_{new_c}.txt"
            new_img_path = os.path.join(output_images_folder, new_img_name)
            new_lbl_path = os.path.join(output_labels_folder, new_lbl_name)
            
            if os.path.exists(new_img_path) or os.path.exists(new_lbl_path):
                current_c += 1
            else:
                old_img_path = os.path.join(images_folder, img_file)
                old_lbl_path = os.path.join(labels_folder, lbl_file)
                shutil.move(old_img_path, new_img_path)
                shutil.move(old_lbl_path, new_lbl_path)
                current_c += 1
                break
    return current_c

def rename_and_move_files(base_dir, output_images_folder, output_labels_folder):
    b_folders = get_b_folders(base_dir)
    current_c = 0
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_labels_folder, exist_ok=True)
    
    for folder_name, _ in b_folders:
        print(f"Renaming files in folder: {folder_name}")
        images_folder = os.path.join(base_dir, folder_name, "images", "train")
        labels_folder = os.path.join(base_dir, folder_name, "labels", "train")
        
        if os.path.exists(images_folder) and os.path.exists(labels_folder):
            current_c = move_files_in_folder(images_folder, labels_folder, current_c, output_images_folder, output_labels_folder)
        else:
            print(f"Skipping folder {folder_name}: 'images/train' or 'labels/train' not found.")

if __name__ == "__main__":
    folder_path = "/home/haithem-ge/wajahat/zip/" #"C:/Users/LAMBDA THETA/Downloads/remain" #
    unzip_folder = "/home/haithem-ge/wajahat/zip/unzip/"#"C:/Users/LAMBDA THETA/Downloads/remain/unzip" #
    output_images_folder = "/home/haithem-ge/wajahat/pose/test/images/"#"C:/wajahat/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/zip/train/images"#"pose/test/images"#
    output_labels_folder = "/home/haithem-ge/wajahat/pose/test/labels/"#"C:/wajahat/Qiyas_Gaze_Estimation/miscellaneous_yolo_pose/zip/train/labels"#"pose/test/labels"#
    unzip_files_in_folder(folder_path, unzip_folder)
    rename_and_move_files(unzip_folder, output_images_folder, output_labels_folder)
