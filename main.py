import os
import time
from datetime import datetime
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip

# Removed YouTube-specific imports

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

def main():
    try:
        # Removed YouTube authentication

        trends = fetch_trends()
        for idx, trend in enumerate(trends):
            # Define paths for saving audio and video locally
            output_dir = r"C:\Users\captk\videos"
            os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
            audio_file = os.path.join(output_dir, f"audio_{idx}.mp3")
            video_file = os.path.join(output_dir, f"video_{idx}.mp4")
            trend_text = f"Manifest ANYTHING {trend} in just 10 minutes!"

            print(f"\n[PROCESSING TREND] {trend}")
            generate_audio(trend_text, audio_file)
            create_video(audio_file, video_file, trend_text)

            # Removed YouTube upload functionality
            
            time.sleep(5)
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
