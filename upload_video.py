import requests

def upload_video(file_path, upload_url):
    """
    Uploads a video file to a server or platform using HTTP POST.

    Args:
    - file_path (str): Path to the video file to upload.
    - upload_url (str): The API endpoint for video uploads.

    Returns:
    - Response object from the upload request.
    """
    try:
        with open(file_path, "rb") as video_file:
            print(f"Uploading {file_path} to {upload_url}...")
            files = {"file": video_file}
            response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            print("Video uploaded successfully!")
        else:
            print(f"Failed to upload video. Status code: {response.status_code}")
            print(f"Response: {response.text}")

        return response

    except FileNotFoundError:
        print(f"[ERROR] The file {file_path} does not exist.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Path to the video file to upload
    file_path = "output_video.mp4"  # Replace with the actual path to your video file

    # Replace with your upload URL
    upload_url = "https://example.com/upload"  # Replace with your upload endpoint

    # Upload the video
    upload_video(file_path, upload_url)
