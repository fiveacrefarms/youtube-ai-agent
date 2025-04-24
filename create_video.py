import os
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
)
import pyttsx3

# Paths to assets
VIDEO_CLIPS_DIR = "video_clips"
BACKGROUND_MUSIC = "background_music.mp3"
SCRIPT_FILE = "script.txt"
OUTPUT_VIDEO = "output_video.mp4"

def text_to_speech(script, output_audio="voiceover.mp3"):
    """
    Convert the script to speech and save as an audio file.
    """
    print("[INFO] Generating voiceover...")
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 150)  # Adjust narration speed if needed
    tts_engine.save_to_file(script, output_audio)
    tts_engine.runAndWait()
    print(f"[INFO] Voiceover saved to {output_audio}")
    return output_audio

def create_scrolling_text(script, duration, video_size):
    """
    Create scrolling captions from the script that match the narration.
    """
    print("[INFO] Creating scrolling text...")
    text_clip = TextClip(script, fontsize=24, color="white", size=video_size, bg_color="black", method="caption")
    scrolling_text = text_clip.set_position(("center", "bottom")).set_duration(duration)
    return scrolling_text

def assemble_video():
    """
    Assemble video clips with voiceover, background music, and synchronized captions.
    """
    print("[INFO] Loading video clips...")
    video_clips = [
        VideoFileClip(os.path.join(VIDEO_CLIPS_DIR, clip))
        for clip in os.listdir(VIDEO_CLIPS_DIR) if clip.endswith(".mp4")
    ]
    final_video = concatenate_videoclips(video_clips, method="compose")

    # Load script
    with open(SCRIPT_FILE, "r") as f:
        script = f.read()

    # Generate voiceover and scrolling captions
    voiceover_audio = text_to_speech(script)
    scrolling_text = create_scrolling_text(script, final_video.duration, final_video.size)

    # Add background music and overlay captions
    background_music = AudioFileClip(BACKGROUND_MUSIC).set_duration(final_video.duration)
    final_video = CompositeVideoClip([final_video, scrolling_text]).set_audio(background_music)

    print("[INFO] Saving final video...")
    final_video.write_videofile(OUTPUT_VIDEO, fps=24, codec="libx264", audio_codec="aac")
    print(f"[INFO] Video saved to {OUTPUT_VIDEO}")

if __name__ == "__main__":
    assemble_video()
