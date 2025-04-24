import subprocess
import os
import sys

def run_script(script_name):
    """
    Runs a Python script using subprocess.
    :param script_name: The name of the Python script to run.
    """
    try:
        print(f"[INFO] Running {script_name}...")
        subprocess.run(["python", script_name], check=True)
        print(f"[INFO] {script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to execute {script_name}.")
        print(e)
       
def main():
   
    print("[INFO] Starting the vlog automation pipeline...")
    
    # Step 1: Generate the vlog script
    if os.path.exists("generate_script.py"):
        print("[INFO] Running generate_script.py...")
        run_script("generate_script.py")
    

    # Step 2: Assemble the video
    if os.path.exists("create_video.py"):
        print("[INFO] Running create_video.py...")
        run_script("create_video.py")
   

    # Step 3: Upload the video to YouTube
    if os.path.exists("upload_video.py"):
        print("[INFO] Running upload_video.py...")
        run_script("upload_video.py")
    

    print("[INFO] Pipeline completed successfully!")

if __name__ == "__main__":
    main()
