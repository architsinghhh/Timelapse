@echo off
echo Running sort.py...
python E:\Archit\sort.py
if %ERRORLEVEL% NEQ 0 (
    echo sort.py encountered an error. Exiting.
    exit /B 1
)

echo Running extract_frame.py...
python E:\Archit\frame_capture.py
if %ERRORLEVEL% NEQ 0 (
    echo extract_frame.py encountered an error. Exiting.
    exit /B 1
)

echo Running timelapse.py...
python E:\Archit\timelapse.py
if %ERRORLEVEL% NEQ 0 (
    echo timelapse.py encountered an error. Exiting.
    exit /B 1
)

echo All scripts completed successfully.
