import os
import re
import time
import cv2
import yaml

# Load configuration from YAML
def load_config():
    """Load configuration from the YAML file."""
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

# Load configuration
config = load_config()
frames_dir = config['paths']['timelapse_frames_dir']
output_video_path = config['paths']['timelapse_output_video']
fps = config['settings']['timelapse_fps']

# Frame settings
frame_size = None  # Set after reading the first frame

# Debugging: Check if directory exists
if not os.path.exists(frames_dir):
    print(f"Error: Directory {frames_dir} does not exist.")
else:
    print(f"Reading frames from directory: {frames_dir}")

# Get sorted list of frame files
frame_files = sorted(
    [f for f in os.listdir(frames_dir) if re.match(r'frame_\d+\.png', f)],
    key=lambda x: int(re.search(r'\d+', x).group())
)

# Debugging: Check number of frames found
print(f"Number of frames found: {len(frame_files)}")
if not frame_files:
    print("No frames found. Check if your frame files are named correctly.")
else:
    # Initialize video writer (after setting frame size from the first frame)
    first_frame_path = os.path.join(frames_dir, frame_files[0])
    first_frame = cv2.imread(first_frame_path)
    
    # Check if the first frame was loaded correctly
    if first_frame is None:
        print(f"Error: Unable to read the first frame at {first_frame_path}.")
    else:
        frame_size = (first_frame.shape[1], first_frame.shape[0])  # Width, Height
        video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)
        print(f"Output video will be saved as {output_video_path} with size {frame_size}.")

        # Start timing
        start_time = time.time()

        # Read each frame in order and write it to the video
        for frame_file in frame_files:
            frame_path = os.path.join(frames_dir, frame_file)
            frame = cv2.imread(frame_path)

            # Only add to video if the frame was loaded successfully
            if frame is not None:
                video_writer.write(frame)
            else:
                print(f"Skipping missing or unreadable frame: {frame_file}")

        # Release the video writer
        video_writer.release()
        
        # End timing
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Timelapse video saved to {output_video_path}.")
        print(f"Total processing time: {total_time:.2f} seconds.")
        
        # Estimate time per frame
        average_time_per_frame = total_time / len(frame_files)
        estimated_time_seconds = average_time_per_frame * len(frame_files)
        print(f"Estimated time per frame: {average_time_per_frame:.4f} seconds.")
        print(f"Estimated total time for {len(frame_files)} frames: {estimated_time_seconds:.2f} seconds.")
