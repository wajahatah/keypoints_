from ultralytics import YOLO
import os
import cv2

# Avoid potential library conflicts
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if __name__ == "__main__":
    # Load your trained YOLOv8 model
    model = YOLO("runs/pose/train25/weights/best.pt")

    # Open the video file
    video_path = "Cam_19_14.mp4"
    cap = cv2.VideoCapture(video_path)

    # Get video properties for saving the output video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video
    out = cv2.VideoWriter('output_with_keypoints.mp4', fourcc, fps, (frame_width, frame_height))

    # Open a text file to save keypoints
    with open('keypoints_output.txt', 'w') as f:

        # Check if the video capture opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        frame_count = 0  # To track frame number

        # Read and process the video frame by frame
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Exit the loop if no more frames are available

            # Run inference on the current frame
            frame = cv2.resize(frame,(1280,720))
            results = model(frame)

            # Iterate over each detected object and print their keypoints
            for result in results:
                keypoints = result.keypoints  # Access the keypoints object

                if keypoints is not None:
                    # Get the data attribute, which contains x, y, and confidence values
                    keypoints_data = keypoints.data
                    for person_idx, person_keypoints in enumerate(keypoints_data):
                        f.write(f"Frame {frame_count}, Person {person_idx}:\n")
                        for kp_idx, keypoint in enumerate(person_keypoints):
                            x, y, confidence = keypoint[0].item(), keypoint[1].item(), keypoint[2].item()

                            # Save the keypoints to the text file
                            f.write(f"  Keypoint {kp_idx}: (x={x:.2f}, y={y:.2f}, confidence={confidence:.2f})\n")

                            # Draw a circle at each keypoint
                            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)

                            # Put the keypoint values on the frame
                            cv2.putText(
                                frame,
                                f"({int(x)}, {int(y)}, {confidence:.2f})",
                                (int(x) + 5, int(y) - 5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.4,
                                (255, 0, 0),
                                1
                            )

            # Write the processed frame to the output video file
            out.write(frame)

            # Display the frame with keypoints and values
            cv2.imshow('Pose Detection', frame)

            # Delay of 50 milliseconds to slow down the video playback
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

            frame_count += 1  # Increment frame counter

    # Release the video capture and close display window
    cap.release()
    out.release()
    cv2.destroyAllWindows()
