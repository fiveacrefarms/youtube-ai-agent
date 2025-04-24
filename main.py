import subprocess
import os
import sys

def run_script(script_name):
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"[INFO] {script_name} ran successfully.")
        print(result.stdout)  # Print the output of the script for debugging
   

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
