import os
from datetime import datetime
from pytrends.request import TrendReq
from gtts import gTTS
from moviepy import TextClip, AudioFileClip, VideoFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Step 1: Fetch Google Trends
def fetch_trends():
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=["manifestation", "inner voice", "my purpose"], geo="US", timeframe="now 3-d")
    trends = pytrends.trending_searches(pn="united_states")
    return trends[0].head(3).values.tolist()

text = "THIS is stopping manifestation or your DESIRED reality!"
# Step 2: Generate Text-to-Speech
def generate_audio(text, audio_0.mp3):
    tts = gTTS(text=text, lang="en")
    tts.save(text_0.mp3)

# Step 3: Create Faceless Video
def create_video(audio_0.mp3, ytv_0.mp4, text):
    # Create a text clip
    text_clip = TextClip(text, fontsize=70, color="white", size=(1280, 720), bg_color="black")
    text_clip = text_clip.set_duration(10)  # 10 seconds per slide

    # Add audio to the text clip
    audio = AudioFileClip(audio_0.mp3)
    video = text_clip.set_audio(audio)

    # Export the video
    video.write_videofile(ytv_0.mp4, fps=24)
video_file = "ytv_0.mp4"

# Step 4: Upload Video to YouTube
def upload_to_youtube(video_file, "THIS is stopping manifestation" , "Yon need to see this NOW"):
    # Authenticate with YouTube API
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"  # Download this from Google Cloud Console

    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

    # Prepare the video metadata
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": ["trending", "news", "AI-generated"]
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    # Upload the video
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)
    response = request.execute()
    print(f"Uploaded video with ID: {response['id']}")

# Step 5: Main Logic
def main():
    trends = fetch_trends()

    for i, trend in enumerate(trends):
        trend_text = f"Here's what trending: {trend}"
        audio_file = f"audio_{i}.mp3"
        video_file = f"video_{i}.mp4"

        # Generate audio
        generate_audio(trend_text, audio_file)

        # Create video
        create_video(audio_file, video_file, trend_text)

        # Upload to YouTube
        upload_to_youtube(video_file, trend, f"Latest trend on {datetime.now().strftime('%Y-%m-%d')}")

        # Cleanup
        os.remove(audio_file)
        os.remove(video_file)

if __name__ == "__main__":
    main()
