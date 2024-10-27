import os
import cv2
import yaml
from glob import glob
from tqdm import tqdm

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config("config.yaml")

def create_dir(path):
    """Create a directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f"ERROR: Failed to create directory '{path}' - {e}")

def resize_frame(frame, width=1920, height=1080):
    """Resize the frame to the specified width and height."""
    return cv2.resize(frame, (width, height))

def save_frames_from_videos(video_paths, save_dir, interval_minutes=5, frame_width=1920, frame_height=1080):
    """Capture frames from videos at specified intervals and save them to a common directory."""
    create_dir(save_dir)  # Ensure the save directory exists

    frame_counter = 0  # To ensure unique filenames for each frame

    for video_path in tqdm(video_paths, desc="Processing videos"):
        cap = cv2.VideoCapture(video_path)
        
        # Validate if video file was opened successfully
        if not cap.isOpened():
            print(f"Error: Cannot open the video file {video_path}")
            continue

        # Get frames per second (fps) and total frame count
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_minutes * 60)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\nProcessing '{video_path}': FPS={fps}, Frame Interval={frame_interval} frames, Total Frames={total_frames}")

        idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Save frame at specified intervals
            if idx % frame_interval == 0:
                resized_frame = resize_frame(frame, width=frame_width, height=frame_height)
                frame_filename = os.path.join(save_dir, f"frame_{frame_counter:06}.png")
                cv2.imwrite(frame_filename, resized_frame)
                print(f"Saved frame {frame_counter} to {frame_filename}")
                frame_counter += 1
            
            idx += 1

        cap.release()
        print(f"Completed frame extraction for '{video_path}'.")

if __name__ == "__main__":
    # Load configuration from YAML
    config = load_config("config.yaml")
    print("Loaded configuration:", config)  # Add this line to debug
    
    # Generate video paths based on config
    video_paths = sorted(glob(os.path.join(config["paths"]["video_dir"], f"*{config['settings']['file_extension']}")))
    save_dir = config["paths"]["save_dir"]

    # Process videos with settings from the YAML file
    save_frames_from_videos(
        video_paths=video_paths,
        save_dir=save_dir,
        interval_minutes=config["settings"]["interval_minutes"],
        frame_width=config["settings"]["frame_width"],
        frame_height=config["settings"]["frame_height"]
    )