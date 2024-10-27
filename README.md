# Timelapse

There are three Python scripts in total; each script's name indicates its functions, such as sort.py allows us to sort the videos based on the working hours, which are 9:00 to 21:00, and store them to a specified folder, followed by the script frame_capture.py, which takes frames from the sorted videos, and the final script timelapse.py generates a timelapse at 60 frames per second.

How to run the process:
To launch the procedure, modify the config.yaml file by changing the paths for metadata, data storage, and extracting frames for timelapse creation.
Run the run_all.bat file; if it doesn't execute directly and redirects to the terminal, specify the path of the python scripts and .yaml file, run run_all.bat in the terminal; it will start executing 
Once completed, a timelapse will be generated.
