import os
import subprocess
import pyttsx3

# Paths to assets
VIDEO_CLIPS_DIR = "video_clips"
BACKGROUND_MUSIC = "background_music.mp3"
SCRIPT_FILE = "script.txt"
OUTPUT_VIDEO = "output_video.mp4"
VOICEOVER_AUDIO = "voiceover.mp3"
CAPTIONS_FILE = "captions.srt"


def text_to_speech(script, output_audio=VOICEOVER_AUDIO):
    """
    Convert the script to speech and save it as an audio file.
    """
    print("[INFO] Generating voiceover...")
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 150)  # Adjust narration speed if needed
    tts_engine.save_to_file(script, output_audio)
    tts_engine.runAndWait()
    print(f"[INFO] Voiceover saved to {output_audio}")


def create_captions(script):
    """
    Create a simple captions file (SubRip Subtitle - .srt format) based on the script.
    Each sentence gets a 5-second duration for simplicity.
    """
    print("[INFO] Generating captions...")
    lines = script.split('. ')
    with open(CAPTIONS_FILE, "w") as f:
        start_time = 0
        for i, line in enumerate(lines, start=1):
            end_time = start_time + 5  # Each caption lasts 5 seconds
            start = f"{start_time//60:02}:{start_time%60:02},000"
            end = f"{end_time//60:02}:{end_time%60:02},000"
            f.write(f"{i}\n{start} --> {end}\n{line.strip()}\n\n")
            start_time = end_time
    print(f"[INFO] Captions saved to {CAPTIONS_FILE}")


def concatenate_clips(output_file="concatenated.mp4"):
    """
    Concatenate video clips in the VIDEO_CLIPS_DIR into a single video.
    Use ffmpeg to handle the concatenation.
    """
    print("[INFO] Concatenating video clips...")
    with open("file_list.txt", "w") as f:
        for clip in sorted(os.listdir(VIDEO_CLIPS_DIR)):
            if clip.endswith(".mp4"):
                f.write(f"file '{os.path.join(VIDEO_CLIPS_DIR, clip)}'\n")

    # Use ffmpeg to concatenate the clips
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "file_list.txt",
        "-c", "copy", output_file
    ], check=True)
    print(f"[INFO] Concatenated video saved to {output_file}")


def add_audio_and_captions(video_file, audio_file, captions_file, output_file):
    """
    Combine video, background music, and captions into the final output video.
    """
    print("[INFO] Adding audio and captions to the video...")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_file, "-i", audio_file, "-vf", f"subtitles={captions_file}",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", output_file
    ], check=True)
    print(f"[INFO] Final video saved to {output_file}")


def assemble_video():
    """
    Assemble the video by combining video clips, voiceover, captions, and background music.
    """
    # Step 1: Load the script
    if not os.path.exists(SCRIPT_FILE):
        print(f"[ERROR] Script file {SCRIPT_FILE} not found!")
        return
    with open(SCRIPT_FILE, "r") as f:
        script = f.read()

    # Step 2: Generate voiceover
    text_to_speech(script)

    # Step 3: Generate captions
    create_captions(script)

    # Step 4: Concatenate video clips
    concatenated_video = "concatenated.mp4"
    concatenate_clips(concatenated_video)

    # Step 5: Add audio and captions to the video
    add_audio_and_captions(concatenated_video, VOICEOVER_AUDIO, CAPTIONS_FILE, OUTPUT_VIDEO)

    print("[INFO] Video assembly completed successfully!")


if __name__ == "__main__":
    assemble_video()
