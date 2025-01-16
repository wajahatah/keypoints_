import cv2

def read_annotations(file_path):
    """Reads annotations from a text file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    annotations = []
    for line in lines:
        values = list(map(float, line.strip().split()))
        
        # Extract frame dimensions (height and width)
        frame_height, frame_width = values[:2]
        
        # Extract head point (x, y, confidence)
        head_x, head_y, head_confidence = values[2:5]
        
        # Extract other keypoints (sets of 3 values: x, y, confidence)
        keypoints = []
        for i in range(5, len(values), 3):
            kp_x, kp_y, confidence = values[i:i + 3]
            keypoints.append((kp_x, kp_y, int(confidence)))
        
        annotations.append({
            "frame_height": frame_height,
            "frame_width": frame_width,
            "head": (head_x, head_y, int(head_confidence)),
            "keypoints": keypoints
        })
    
    return annotations

def draw_annotations(image_path, annotations, output_path):
    """Draws bounding boxes, head points, and keypoints on the image."""
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    for person in annotations:
        # Draw head point
        head_x, head_y, head_confidence = person["head"]
        if head_confidence > 0:  # Draw only if visible
            head_x_px, head_y_px = int(head_x * width), int(head_y * height)
            cv2.circle(image, (head_x_px, head_y_px), 8, (255, 255, 0), -1)  # Yellow for head
            cv2.putText(image, f"Head: ({head_x:.2f}, {head_y:.2f}, {head_confidence})", 
                        (head_x_px + 10, head_y_px - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Draw other keypoints with values
        for i, kp in enumerate(person["keypoints"]):
            kp_x, kp_y, confidence = kp
            if confidence > 0:  # Draw only visible points
                kp_x_px, kp_y_px = int(kp_x * width), int(kp_y * height)
                color = (0, 0, 255) if confidence == 2 else (255, 0, 0)
                cv2.circle(image, (kp_x_px, kp_y_px), 5, color, -1)
                cv2.putText(image, f"{i}: ({kp_x:.2f}, {kp_y:.2f}, {confidence})", 
                            (kp_x_px + 5, kp_y_px - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # Save the output image
    cv2.imwrite(output_path, image)

# Replace these with your file paths
annotation_file = "C:/Users/LAMBDA THETA/Downloads/keypoints/b5_78/labels/train/frame_000000.txt"  # Path to your annotation text file
image_path = "C:/Users/LAMBDA THETA/Downloads/keypoints/b5_78/images/train/frame_000000.PNG"  # Path to your image file
output_path = "C:/Users/LAMBDA THETA/Downloads/plot10.png"  # Path for the output image

# Process the annotations and draw them
annotations = read_annotations(annotation_file)
draw_annotations(image_path, annotations, output_path)
