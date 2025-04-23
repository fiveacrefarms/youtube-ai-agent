import os
from datetime import datetime
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from gtts import gTTS
from moviepy import TextClip, AudioFileClip, VideoFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import time
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError

import logging
logging.basicConfig(level=logging.DEBUG)
# Step 1: Fetch Google Trends
def fetch_google_trends_data(keywords, timeframe="today 2-y"):
   
    pytrends = TrendReq(hl="en-US", tz=360)
    trends_data = {}
    
    for keyword in keywords:
        try:
            print(f"Fetching data for keyword: {keyword}")
            
            # Build payload for the keyword
            pytrends.build_payload([keyword], timeframe=timeframe)
            
            # Fetch interest over time data
            data = pytrends.interest_over_time()
            
            # Save the data to the dictionary
            if not data.empty:
                trends_data[keyword] = data
            else:
                print(f"No data available for keyword: {keyword}")
            
        except ResponseError as e:
            print(f"Error with keyword '{keyword}': {e}")
        
        # Add a delay to avoid rate limiting
        time.sleep(10)
    
    return trends_data


if __name__ == "__main__":
    # Example keywords
    kw_list = ["Quantum Realm", "Meditation", "reality"]
    
    # Fetch data and handle errors
    trends_data = fetch_google_trends_data(kw_list)
    
    # Print the results
    for keyword, data in trends_data.items():
        print(f"\nTrends data for '{keyword}':")
        print(data)
text = "THIS is stopping manifestation or your DESIRED reality!"
# Step 2: Generate Text-to-Speech
def generate_audio(text, audio_path):
    tts = gTTS(text=text, lang="en")
    tts.save("text_0.mp3")

# Step 3: Create Faceless Video
def create_video(audio_path, output_path, text):
    # Create a text clip
    text_clip = TextClip(text, fontsize=70, color="white", size=(1280, 720), bg_color="black")
    text_clip = text_clip.set_duration(10)  # 10 seconds per slide

    # Add audio to the text clip
    audio = AudioFileClip(audio_path)
    video = text_clip.set_audio(audio)

    # Export the video
    video.write_videofile(output_path, fps=24)
video_file = "ytv_0.mp4"

# Step 4: Upload Video to YouTube
def upload_to_youtube(video_file, title, description):
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
        audio_file = f"audio_{0}.mp3"
        video_file = f"video_{0}.mp4"

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
