import os
import requests

def upload_video(video_clips, upload_url):
    """
    Uploads video clips to a server or platform using HTTP POST.

    Args:
    - video_clips (list): List of video file paths to upload.
    - upload_url (str): The API endpoint for video uploads.
    """
    for file_path in video_clips:
        if not os.path.exists(file_path):
            print(f"[ERROR] The file {file_path} does not exist.")
            continue

        try:
            with open(file_path, "rb") as file:  # Using 'file' to avoid introducing new names
                print(f"Uploading {file_path} to {upload_url}...")
                files = {"file": file}  # Keep the key as "file" unless the API requires a different key
                response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                print(f"Video {file_path} uploaded successfully!")
            else:
                print(f"Failed to upload {file_path}. Status code: {response.status_code}")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while uploading {file_path}: {e}")

if __name__ == "__main__":
    # List of video clips to upload
    video_clips = ["video_clips/output_video.mp4", "video_clips/segment_0.mp4"]  # Example: Replace with actual paths

    # Upload endpoint
    upload_url = "https://example.com/upload"  # Replace with your API endpoint

    # Upload the video clips
    upload_video(video_clips, upload_url)
