import subprocess
import os
import sys

def run_script(script_name):
    """
    Runs a Python script as a subprocess and checks for errors.
    """
    try:
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"[INFO] {script_name} ran successfully.")
        print(result.stdout)  # Print the output of the script for debugging
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to execute {script_name}.")
        print(f"[ERROR] {e.stderr}")
        sys.exit(1)

def main():
    """
    Orchestrates the pipeline by running all scripts in sequence.
    """
    print("[INFO] Starting the vlog automation pipeline...")
    
    # Step 1: Generate the vlog script
    if os.path.exists("generate_script.py"):
        print("[INFO] Running generate_script.py...")
        run_script("generate_script.py")
    else:
        print("[ERROR] Missing generate_script.py. Make sure it exists.")
        sys.exit(1)

    # Step 2: Assemble the video
    if os.path.exists("create_video.py"):
        print("[INFO] Running create_video.py...")
        run_script("create_video.py")
    else:
        print("[ERROR] Missing create_video.py. Make sure it exists.")
        sys.exit(1)

    # Step 3: Upload the video to YouTube
    if os.path.exists("upload_video.py"):
        print("[INFO] Running upload_video.py...")
        run_script("upload_video.py")
    else:
        print("[ERROR] Missing upload_video.py. Make sure it exists.")
        sys.exit(1)

    print("[INFO] Pipeline completed successfully!")

if __name__ == "__main__":
    main()
