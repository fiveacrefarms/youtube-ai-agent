import os
from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip

# Define constants
OUTPUT_DIR = r"C:\Users\captk\youtube-ai-agent\build\artifacts"
TRENDS = ["Abundance", "Meditation", "Manifest Anything"]

def fetch_trends():
    """
    Fetch the trends for video generation.
    Returns:
        list: A list of trending topics.
    """
    return TRENDS

def generate_audio(text, audio_path):
    """
    Generate an audio file using Google Text-to-Speech (gTTS).
    Args:
        text (str): The text to be converted into speech.
        audio_path (str): The path to save the audio file.
    """
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)
        print(f"[AUDIO GENERATED] {audio_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate audio: {e}")

def create_video(audio_path, video_path, text):
    """
    Create a video file with text overlay and audio.
    Args:
        audio_path (str): The path to the audio file.
        video_path (str): The path to save the video file.
        text (str): The text to display in the video.
    """
    try:
        # Create a text clip
        text_clip = TextClip(
            text,
            fontsize=50,
            color="white",
            size=(1280, 720),
            bg_color="black"
        ).set_duration(10)  # Duration in seconds

        # Load the audio file
        audio = AudioFileClip(audio_path)

        # Combine text and audio into a video
        video = CompositeVideoClip([text_clip]).set_audio(audio)
        video.write_videofile(video_path, fps=24)
        print(f"[VIDEO CREATED] {video_path}")
    except Exception as e:
        print(f"[ERROR] Failed to create video: {e}")

def main():
    """
    Main function to generate videos based on trending topics.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Fetch trends and generate audio and video files
        trends = fetch_trends()
        for idx, trend in enumerate(trends):
            print(f"\n[PROCESSING TREND] {trend}")

            # Define file paths
            audio_path = os.path.join(OUTPUT_DIR, f"audio_{idx}.mp3")
            video_path = os.path.join(OUTPUT_DIR, f"video_{idx}.mp4")
            trend_text = f"Manifest ANYTHING {trend} in just 10 minutes!"

            # Generate and save audio and video files
            generate_audio(trend_text, audio_path)
            create_video(audio_path, video_path, trend_text)

        print(f"\n[ALL FILES SAVED] Files have been saved to: {OUTPUT_DIR}")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
