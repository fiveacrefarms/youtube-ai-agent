from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API credentials
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secrets.json"

def upload_video(video_file, title, description, tags):
    """
    Upload a video to YouTube.
    """
    print("[INFO] Authenticating with YouTube API...")
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey="YOUR_YOUTUBE_API_KEY")

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"  # Category 22 is for "People & Blogs"
        },
        "status": {
            "privacyStatus": "public"  # Change to "private" if needed
        }
    }

    print("[INFO] Uploading video...")
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(f"[INFO] Video uploaded: {response['id']}")

if __name__ == "__main__":
    upload_video("output_video.mp4", "Daily Inspiration", "An inspiring vlog for your day.", ["vlog", "inspiration", "daily"])
