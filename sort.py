import cv2
import os
import re
import shutil
import yaml
from datetime import datetime

def load_config():
    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load the config
config = load_config()

# Access paths
video_dir = config["paths"]["video_dir"]
output_dir = config["paths"]["output_dir"]
save_dir = config["paths"]["save_dir"]

# Access settings
interval_minutes = config["settings"]["interval_minutes"]
frame_width = config["settings"]["frame_width"]
frame_height = config["settings"]["frame_height"]
work_start_time = config["settings"]["work_start_time"]
work_end_time = config["settings"]["work_end_time"]

# Access patterns
mp4_pattern = config["patterns"]["mp4_pattern"]
dav_pattern = config["patterns"]["dav_pattern"]

# Define the file extensions to filter
file_extensions = (".mp4", ".DAV")  # Add more extensions if needed

def parse_filename(filename):
    """Parse the filename and return start and end datetimes."""
    if filename.endswith(".mp4"):
        match = re.search(mp4_pattern, filename)
    elif filename.endswith(".DAV"):
        match = re.search(dav_pattern, filename)
    else:
        return None, None

    if match:
        start_date, start_time, end_date, end_time = match.groups()
        start_datetime = datetime.strptime(start_date + start_time, "%Y%m%d%H%M%S")
        end_datetime = datetime.strptime(end_date + end_time, "%Y%m%d%H%M%S")
        return start_datetime, end_datetime
    return None, None

def is_within_working_hours(start_time, end_time):
    """Check if the video overlaps with the working hours from config."""
    work_start = datetime.strptime(work_start_time, "%H:%M:%S").time()
    work_end = datetime.strptime(work_end_time, "%H:%M:%S").time()

    start_in_range = start_time.time() <= work_end and start_time.time() >= work_start
    end_in_range = end_time.time() <= work_end and end_time.time() >= work_start
    overlaps_range = (start_time.time() <= work_start and end_time.time() >= work_start) or \
                     (start_time.time() <= work_end and end_time.time() >= work_end)
    return start_in_range or end_in_range or overlaps_range

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Filter and sort files based on working hours
sorted_files = []
for file in os.listdir(video_dir):
    if file.endswith(file_extensions):
        start_time, end_time = parse_filename(file)
        if start_time and end_time and is_within_working_hours(start_time, end_time):
            sorted_files.append((start_time, end_time, file))

# Sort files by start time
sorted_files.sort(key=lambda x: x[0])

# Copy filtered files to the new folder
# Copy filtered files to the new folder
for _, _, file in sorted_files:
    src_path = os.path.join(video_dir, file)
    dest_path = os.path.join(output_dir, file)
    
    try:
        print(f"Copying from {src_path} to {dest_path}")
        shutil.copy2(src_path, dest_path)  # Copies file with metadata
        print(f"Copied {file} to {output_dir}")
    except Exception as e:
        print(f"Error copying {file}: {e}")


# Optional: Process each video file with OpenCV if needed
for _, _, file in sorted_files:
    video_path = os.path.join(output_dir, file)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video {file}")
        continue
    # Process video frames as needed
    # ...
    cap.release()
