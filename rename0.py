import os

def rename_files_with_text_and_number(text_folder, image_folder, text_extension=".txt", image_extension=".jpg", start_number=142, custom_text="frame", new_name_pattern="{}_{:05d}"):
    """
    Rename text and image files that have the same original name, with both custom text and number.

    Parameters:
    - text_folder: Folder where text files are stored.
    - image_folder: Folder where image files are stored.
    - text_extension: Extension of the text files (e.g., '.txt').
    - image_extension: Extension of the image files (e.g., '.jpg').
    - start_number: Starting number for the new filenames.
    - custom_text: Custom text to include in the new filenames.
    - new_name_pattern: Pattern for renaming files (e.g., '{}_{:05d}' where '{}' is replaced by custom_text).
    """
    # Get a list of text and image filenames (without extension)
    text_files = {os.path.splitext(f)[0] for f in os.listdir(text_folder) if f.endswith(text_extension)}
    image_files = {os.path.splitext(f)[0] for f in os.listdir(image_folder) if f.endswith(image_extension)}

    # Find the common base names between text and image files
    common_files = text_files.intersection(image_files)

    current_number = start_number  # Set the starting number for the new filenames

    for base_name in common_files:
        # Create new name using the custom text and current number
        new_name = new_name_pattern.format(custom_text, current_number)

        # Get old file paths
        old_text_file = os.path.join(text_folder, base_name + text_extension)
        old_image_file = os.path.join(image_folder, base_name + image_extension)

        # Get new file paths
        new_text_file = os.path.join(text_folder, new_name + text_extension)
        new_image_file = os.path.join(image_folder, new_name + image_extension)

        # Rename the text file
        if os.path.exists(old_text_file):
            os.rename(old_text_file, new_text_file)
            print(f"Renamed text file: {old_text_file} -> {new_text_file}")
        else:
            print(f"Text file not found: {old_text_file}")

        # Rename the image file
        if os.path.exists(old_image_file):
            os.rename(old_image_file, new_image_file)
            print(f"Renamed image file: {old_image_file} -> {new_image_file}")
        else:
            print(f"Image file not found: {old_image_file}")

        # Increment the current number for the next set of files
        current_number += 1

# Example usage:
text_folder = "C:/Users/LAMBDA THETA/Downloads/b5_2/train/labels"   # Folder where the text files are stored
image_folder = "C:/Users/LAMBDA THETA/Downloads/b5_2/train/images/default" # Folder where the image files are stored

# Rename files with a custom text and starting number, e.g., 'customText_00100.txt' and 'customText_00100.jpg'
rename_files_with_text_and_number(text_folder, image_folder, start_number=142, custom_text="frame")
