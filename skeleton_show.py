import json
import matplotlib.pyplot as plt
import os
from PIL import Image
import matplotlib.patches as patches

# Map of COCO keypoint index to their names
KEYPOINT_NAMES = [
    "Head", "neck", "left_ear", "right_ear", 
    "left_shoulder", "left_arm", "left_wrist", "right_shoulder", "right_arm", "right_wrist"
]

def parse_coco_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    frames_data = {}

    # Map image ids to file names
    images_dict = {image['id']: image for image in data['images']}

    # Parse all annotations (keypoints and bounding boxes)
    for annotation in data['annotations']:
        image_id = annotation['image_id']
        if image_id not in images_dict:
            continue
        
        image_info = images_dict[image_id]
        file_name = image_info['file_name']
        
        # Create a dictionary entry for each image if it doesn't exist
        if image_id not in frames_data:
            frames_data[image_id] = {
                'file_name': file_name,
                'width': image_info['width'],
                'height': image_info['height'],
                'annotations': []  # List to hold annotations for this image
            }

        # Add the current annotation to the list for this image
        frames_data[image_id]['annotations'].append({
            'keypoints': annotation['keypoints'],
            'bbox': annotation['bbox']
        })

    return list(frames_data.values())

def plot_skeleton_on_image(frame_data, image_folder, save_folder):
    img_path = os.path.join(image_folder, frame_data['file_name'])

    # Debugging print to show the image path being used
    print(f"Looking for image at: {img_path}")

    # Check if the image exists
    if not os.path.exists(img_path):
        print(f"Image {img_path} not found.")
        return

    img = Image.open(img_path)
    plt.figure(figsize=(10, 5))
    
    # Show the image
    plt.imshow(img)

    # Extract the bounding boxes and keypoints for all annotations
    for annotation in frame_data['annotations']:
        bbox = annotation['bbox']
        keypoints = annotation['keypoints']
        
        # Unpack bounding box data (COCO format: [x, y, width, height])
        bbox_x, bbox_y, bbox_w, bbox_h = bbox
        padding = 10  # Padding for a more visible bounding box

        # Create a padded rectangle patch for the bounding box
        rect = patches.Rectangle((bbox_x - padding, bbox_y - padding), bbox_w + 2 * padding, bbox_h + 2 * padding, 
                                 linewidth=2, edgecolor='green', facecolor='none')
        plt.gca().add_patch(rect)

        # Plot the keypoints (COCO keypoints: [x, y, v] where v is visibility)
        for i in range(0, len(keypoints), 3):
            x, y, v = keypoints[i:i+3]
            if v > 0:  # v > 0 means the keypoint is visible
                plt.scatter(x, y, color='red', s=40)
                kp_name = KEYPOINT_NAMES[i//3] if i//3 < len(KEYPOINT_NAMES) else f'Point {i//3}'
                plt.text(x + 10, y + 10, kp_name, fontsize=8, color='yellow', weight='bold')

    plt.title(f"Image {frame_data['file_name']}")

    # Save the result
    save_path = os.path.join(save_folder, f"skeleton_{frame_data['file_name']}")
    plt.savefig(save_path)
    plt.close()

def visualize_frames_on_images(frames_data, image_folder, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    for frame_data in frames_data:
        plot_skeleton_on_image(frame_data, image_folder, save_folder)

if __name__ == "__main__":
    # Path to your COCO 1.1 JSON file
    json_file = r"C:/Users/LAMBDA THETA/Downloads/b5_1/annotations/person_keypoints_default.json"
    
    # Path to the folder containing the images
    image_folder = r"C:/Users/LAMBDA THETA/Downloads/b5_1/images/default"
    
    # Folder where the resulting images with skeletons will be saved
    save_folder = r"C:/Users/LAMBDA THETA/Downloads/b5_1/output"
    
    # Parse the COCO JSON file
    frames_data = parse_coco_json(json_file)
    
    # Visualize skeletons overlaid on images
    visualize_frames_on_images(frames_data, image_folder, save_folder)
