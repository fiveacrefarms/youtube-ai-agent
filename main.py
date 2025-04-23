import os
import time
from datetime import datetime
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery_cache.base import Cache

class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return self._CACHE.get(url)

    def set(self, url, content):
        self._CACHE[url] = content

def fetch_trends():
    return ["Abundance", "Meditation", "Manifest Anything"]

def generate_audio(text, audio_path):
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)
        print(f"[AUDIO GENERATED] {audio_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate audio: {e}")

def create_video(audio_path, video_path, text):
    try:
        text_clip = TextClip(text, fontsize=50, color="white", size=(1280, 720), bg_color="black")
        text_clip = text_clip.set_duration(10)
        audio = AudioFileClip(audio_path)
        video = text_clip.set_audio(audio)
        video.write_videofile(video_path, fps=24)
        print(f"[VIDEO CREATED] {video_path}")
    except Exception as e:
        print(f"[ERROR] Failed to create video: {e}")

def authenticate_youtube():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(".gitignore/client_secrets2.json", scopes=["https://www.googleapis.com/auth/youtube.upload"])
        credentials = flow.run_console()
        youtube = build("youtube", "v3", credentials=credentials, cache=MemoryCache())
        return youtube
    except Exception as e:
        print(f"[ERROR] YouTube authentication failed: {e}")
        return None

def upload_to_youtube(youtube, video_file, title, description):
    try:
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["Abundance", "Meditation", "Manifest Anything"],
                "categoryId": "24"
            },
            "status": {
                "privacyStatus": "public"
            }
        }
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        upload_request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )
        response = upload_request.execute()
        print(f"[UPLOAD SUCCESSFUL] Video ID: {response['id']}")
    except Exception as e:
        print(f"[ERROR] Failed to upload video: {e}")

def main():
    try:
        youtube = authenticate_youtube()
        if not youtube:
            print("[ERROR] Exiting due to failed YouTube authentication.")
            return

        trends = fetch_trends()
        for idx, trend in enumerate(trends):
            audio_file = f"audio/audio_{idx}.mp3"
            video_file = f"video/video_{idx}.mp4"
            trend_text = f"Manifest ANYTHING {trend} in just 10 minutes!"

            print(f"\n[PROCESSING TREND] {trend}")
            generate_audio(trend_text, audio_file)
            create_video(audio_file, video_file, trend_text)
            title = f"Windows Tips: {trend}"
            description = f"Live in total {trend}. This video will help you!"
            upload_to_youtube(youtube, video_file, title, description)
           
            time.sleep(5)
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
