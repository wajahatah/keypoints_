import os

def rearrange_keypoints(input_folder, output_folder):
    """
    Rearranges key points in annotation files from the input folder
    and saves the modified files in the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r') as file:
            lines = file.readlines()

        modified_annotations = []
        for line in lines:
            # values = list(map(float, line.strip().split()))
            values = line.strip().split()

            # Extract basic annotation details
            class_id = int(values[0])
            center_x, center_y, frame_height, frame_width = map(float, values[1:5])
            # center_x, center_y = values[1:3]
            # frame_height, frame_width = values[3:5]
            
            # Extract keypoints
            # keypoints = values[5:]
            keypoints=[]
            for i in range(5, len(values),3):
                x,y,confidence = values[i:i+3]
                keypoints.append((float(x),float(y),int(confidence)))

            head = keypoints[0]
            left_ear = keypoints[1]
            right_ear = keypoints[2]
            neck = keypoints[3]
            right_shoulder = keypoints[4]
            left_shoulder = keypoints[5]
            left_elbow = keypoints[6]
            right_elbow = keypoints[7]
            right_hand = keypoints[8]
            left_hand = keypoints[9]
            
            # Rearrange keypoints
            rearranged_keypoints = [
                head, 
                neck,
                left_ear, 
                right_ear,
                left_shoulder, 
                left_elbow, 
                left_hand,
                right_shoulder, 
                right_elbow,
                right_hand
            ]
            
            # Prepare the modified line
            # modified_line = f"{class_id} {center_x:.6f} {center_y:.6f} {frame_height:.6f} {frame_width:.6f} " + \
            #                 " ".join(f"{kp:.6f}" for kp in rearranged_keypoints) + "\n"
            # modified_annotations.append(modified_line)
            modified_line = (
                    f"{class_id} {center_x:.6f} {center_y:.6f} {frame_height:.6f} {frame_width:.6f} " +
                    " ".join(
                        f"{kp[0]:.6f} {kp[1]:.6f} {kp[2]}" for kp in rearranged_keypoints
                    ) + "\n"
                )
            modified_annotations.append(modified_line)

        # Save modified annotations
        with open(output_path, 'w') as file:
            file.writelines(modified_annotations)

input_folder = "C:/Users/LAMBDA THETA/Downloads/keypoints/b5_78/labels/train"  # Folder containing original annotation files
output_folder = "C:/Users/LAMBDA THETA/Downloads/keypoints/b5_78/labels/train1"  # Folder to save modified annotation files

# Call the function
rearrange_keypoints(input_folder, output_folder)

print("Rearrangement complete. Modified files saved to output folder.")

# base_folder = "C:/Users/LAMBDA THETA/Downloads/keypoints"
# output_base_folder = "C:/Users/LAMBDA THETA/Downloads/keypoints_output"

# # Loop through folders in the range
# for folder_number in range(78, 134):  # Range includes b5_78 to b5_129
#     input_folder = os.path.join(base_folder, f"b5_{folder_number}/labels/train")
#     output_folder = os.path.join(output_base_folder, f"b5_{folder_number}/labels/train1")

#     if os.path.exists(input_folder):  # Process only if the folder exists
#         rearrange_keypoints(input_folder, output_folder)
#         print(f"Processed folder: b5_{folder_number}")

# print("Rearrangement complete for all specified folders.")

# # Replace these paths with your folder paths
# base_folder = "C:/Users/LAMBDA THETA/Downloads/keypoints"  # Folder containing original annotation files
# # output_folder = "C:/Users/LAMBDA THETA/Downloads/keypoints/b5_116/labels/train1"  # Folder to save modified annotation files

# for folder_number in range(78,133):
#     input_folder = os.path.join(base_folder, f"b%_{folder_number}/labels/train")
#     output_folder = os.path.join(base_folder, f"b%_{folder_number}/labels/train")
# # Call the function
# rearrange_keypoints(input_folder, output_folder)

# print("Rearrangement complete. Modified files saved to output folder.")
