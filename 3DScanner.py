import serial
import subprocess
import time
import os
import shutil
from datetime import datetime

# --- Settings ---
serial_port = 'COM3'      # Change this to your Arduino's port
baud_rate = 9600
timeout_sec = 2

digicam_path = r"C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe"
digicam_output_folder = r"C:\Users\user\Pictures\digiCamControl\Session1"  # Default save folder of digiCamControl
desired_folder = r"C:\Users\user\Documents\3DScanner\Scan"  # Folder where you want to move images

# Ensure desired folder exists
os.makedirs(desired_folder, exist_ok=True)

# --- Serial Setup ---

ser = serial.Serial(serial_port, baud_rate, timeout=timeout_sec)


# --- Main Loop ---
try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print(f"Arduino: {line}")

            if line == "Image Captured":
                print("Triggering DSLR via digiCamControl...")
                try:
                    # Set a unique name using timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"capture_{timestamp}.jpg"

                    # Trigger capture
                    subprocess.run([digicam_path, "/capture"], check=True)

                    print("Capture done, waiting for file...")

                    # Wait a moment for file to be saved
                    time.sleep(2)

                    # Find the latest image file in digiCamControl folder
                    files = [f for f in os.listdir(digicam_output_folder) if f.lower().endswith('.jpg')]
                    if not files:
                        print("No image files found in digiCamControl folder.")
                        continue

                    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(digicam_output_folder, f)))
                    source_path = os.path.join(digicam_output_folder, latest_file)
                    target_path = os.path.join(desired_folder, filename)

                    # Move and rename the file
                    shutil.move(source_path, target_path)
                    print(f"Image saved to: {target_path}")

                except subprocess.CalledProcessError as e:
                    print(f"Failed to trigger camera: {e}")
                except Exception as e:
                    print(f"Error moving file: {e}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()
