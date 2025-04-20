import os
import time
from gtts import gTTS
from moviepy.editor import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

# Hardcoded data (no APIs)
TRENDS = ["Tech News", "AI Breakthroughs", "Gaming Trends"]
IMAGE_URLS = [
    "https://placehold.co/1920x1080.png?text=Tech+News",
    "https://placehold.co/1920x1080.png?text=AI+Breakthroughs",
    "https://placehold.co/1920x1080.png?text=Gaming+Trends"
]

def create_audio(text, filename):
    os.makedirs("audio", exist_ok=True)
    tts = gTTS(text=text, lang='en')
    tts.save(os.path.join("audio", filename))

def download_image(url, filename):
    os.makedirs("images", exist_ok=True)
    os.system(f"curl -s {url} -o images/{filename}.png")  # Bypass Python requests

def make_video(audio_file, output):
    os.makedirs("videos", exist_ok=True)
    clips = [ImageClip(f"images/{i}.png").set_duration(3) for i in range(3)]
    video = concatenate_videoclips(clips)
    video = video.set_audio(AudioFileClip(audio_file))
    video.write_videofile(os.path.join("videos", output), fps=24, logger=None)

def upload_to_yt(email, password, video_path, title):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://studio.youtube.com")
    
    # Login
    driver.find_element(By.ID, "identifierId").send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(5)
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    time.sleep(5)
    
    # Upload
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(os.path.abspath(video_path))
    time.sleep(5)
    title_field = driver.find_element(By.ID, "textbox")
    title_field.clear()
    title_field.send_keys(title)
    for _ in range(3):
        driver.find_element(By.ID, "next-button").click()
        time.sleep(3)
    driver.find_element(By.ID, "done-button").click()
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    for idx, trend in enumerate(TRENDS):
        # 1. Generate audio
        create_audio(f"Trending: {trend}", f"audio_{idx}.mp3")
        
        # 2. Download images (no API)
        for img_idx, url in enumerate(IMAGE_URLS):
            download_image(url, f"{img_idx}")
        
        # 3. Create video
        make_video(f"audio/audio_{idx}.mp3", f"video_{idx}.mp4")
        
        # 4. Upload to YouTube
        upload_to_yt(
            os.getenv("YT_EMAIL"),
            os.getenv("YT_PASSWORD"),
            f"videos/video_{idx}.mp4",
            f"{trend} - Automated Short"
        )
