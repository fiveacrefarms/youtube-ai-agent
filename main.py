import os
from gtts import gTTS
from moviepy.editor import *
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# STEP 1: Hardcode trends to avoid API errors
def get_trends():
    return ["AI News", "Tech Updates", "Gaming Trends"]

# STEP 2: Generate audio
def create_audio(text, filename):
    os.makedirs("audio", exist_ok=True)
    tts = gTTS(text=text, lang='en')
    tts.save(f"audio/{filename}")

# STEP 3: Fetch images (no external APIs)
def get_images(query):
    return [
        "https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg",  # Static image 1
        "https://images.pexels.com/photos/2486168/pexels-photo-2486168.jpeg", # Static image 2
        "https://images.pexels.com/photos/450035/pexels-photo-450035.jpeg"    # Static image 3
    ]

# STEP 4: Create video
def make_video(images, audio, output):
    os.makedirs("videos", exist_ok=True)
    clips = [ImageClip(img).set_duration(3) for img in images]
    video = concatenate_videoclips(clips)
    video = video.set_audio(AudioFileClip(audio))
    video.write_videofile(f"videos/{output}", fps=24)

# STEP 5: Upload to YouTube
def upload_to_yt(email, password, video_path, title):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://studio.youtube.com")
    
    # Login
    driver.find_element(By.ID, "identifierId").send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    sleep(2)
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    sleep(5)
    
    # Upload
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(os.path.abspath(video_path))
    sleep(5)
    driver.find_element(By.ID, "textbox").send_keys(title)
    for _ in range(3):  # Click "Next" 3 times
        driver.find_element(By.ID, "next-button").click()
        sleep(1)
    driver.find_element(By.ID, "done-button").click()
    sleep(10)
    driver.quit()

if __name__ == "__main__":
    trends = get_trends()
    for idx, trend in enumerate(trends):
        script = f"Breaking News: {trend} is making waves right now!"
        create_audio(script, f"audio_{idx}.mp3")
        images = get_images(trend)
        make_video(images, f"audio/audio_{idx}.mp3", f"video_{idx}.mp4")
        upload_to_yt(
            os.getenv('YT_EMAIL'),
            os.getenv('YT_PASSWORD'),
            f"videos/video_{idx}.mp4",
            f"{trend} Trending Now!"
        )
