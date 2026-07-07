import cv2
import numpy as np

# Define a function to check if a color is red or blue
def is_red_or_blue(pixel):
    pixel_sum = np.sum(pixel, dtype=np.uint16)  # Use a larger data type for the sum
    average_pixel_value = pixel_sum // 3  # Integer division to avoid potential overflow
    return "black" if average_pixel_value < 128 else "white"
    # Define color thresholds in HSV
    # red_lower = np.array([0, 70, 50])
    # red_upper = np.array([10, 255, 255])
    # blue_lower = np.array([100, 150, 0])
    # blue_upper = np.array([140, 255, 255])
    
    # # Convert the BGR pixel to HSV
    # hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]
    
    # # Check if it's red or blue
    # if (red_lower <= hsv_pixel).all() and (hsv_pixel <= red_upper).all():
    #     return 'red'
    # elif (blue_lower <= hsv_pixel).all() and (hsv_pixel <= blue_upper).all():
    #     return 'blue'
    # return None

# Initialize video capture
video_path = 'asgi_exp_for_video.mp4'  # Replace with the path to your video file
cap = cv2.VideoCapture(video_path)

# Get frame rate to calculate timestamps
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = 0
previous_color = None
transitions = []

# Loop through each frame
prev_frame = None
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    # Extract the bottom-right pixel (change size if needed to a region)
    height, width, _ = frame.shape
    bottom_right_pixel = frame[height - 5, width - 5]
    
    # Check the color of the bottom-right pixel
    current_color = is_red_or_blue(bottom_right_pixel)
    
    # Detect transition if previous color exists and is different
    if previous_color and current_color and previous_color != current_color:
        timestamp = frame_count / fps
        ## Saving transitioning frames for debugging
        # cv2.imwrite(f'frame{len(transitions)+1}_1.jpg', prev_frame)
        # cv2.imwrite(f'frame{len(transitions)+1}_2.jpg', frame)
        transitions.append((timestamp, previous_color, current_color))
    
    # Update previous color
    if current_color:
        previous_color = current_color
    prev_frame = frame

# Release video capture
cap.release()

# Print results
for transition in transitions:
    print(f"Color changed from {transition[1]} to {transition[2]} at {transition[0]:.2f} seconds")
print(len(transitions))
print(fps)
duration = frame_count/fps
print(duration)
print(frame_count)