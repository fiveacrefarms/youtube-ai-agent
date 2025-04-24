import cv2
import os

def split_video(video_path, segment_duration=10):
    """
    Splits a video into segments of a given duration (in seconds).
    """
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_segments = []
    count = 0
    segment_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Create a new video segment file every `segment_duration` seconds
        if count % (fps * segment_duration) == 0:
            if 'out' in locals():
                out.release()
            segment_file = f"segment_{segment_index}.mp4"
            out = cv2.VideoWriter(segment_file, fourcc, fps, (frame_width, frame_height))
            video_segments.append(segment_file)
            segment_index += 1

        out.write(frame)
        count += 1

    if 'out' in locals():
        out.release()
    cap.release()
    return video_segments

def concatenate_videos(video_files, output_file="output_video.mp4"):
    """
    Concatenates a list of video files into one video.
    """
    if not video_files:
        print("[ERROR] No video files to concatenate.")
        return

    # Get the properties of the first video
    cap = cv2.VideoCapture(video_files[0])
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    cap.release()

    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    for video_file in video_files:
        print(f"Processing {video_file}...")
        cap = cv2.VideoCapture(video_file)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()

    out.release()
    print(f"Final video saved as {output_file}")

if __name__ == "__main__":
    # List of video files to concatenate
    video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]  # Replace with your actual video file paths

    all_segments = []

    # Step 1: Split videos into 10-second segments
    for video_file in video_files:
        print(f"Splitting {video_file} into 10-second segments...")
        segments = split_video(video_file, segment_duration=10)
        all_segments.extend(segments)

    # Step 2: Concatenate all segments into a single video
    concatenate_videos(all_segments, output_file="output_video.mp4")
