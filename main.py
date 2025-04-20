import os
from pytrends.request import TrendReq
from gtts import gTTS
from moviepy.editor import *
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv

load_dotenv()

def get_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_topics = pytrends.trending_searches(pn='US')
    return trending_topics.head(3)[0].tolist()

def generate_script(topic):
    return f"Breaking news! {topic} is trending right now. Stay tuned for updates!"

def create_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

def get_images(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=3"
    headers = {"Authorization": os.getenv('PEXELS_KEY')}
    res = requests.get(url, headers=headers).json()
    return [photo['src']['medium'] for photo in res['photos']]

def make_video(images, audio, output):
    clips = [ImageClip(img).set_duration(3) for img in images]
    video = concatenate_videoclips(clips)
    video = video.set_audio(AudioFileClip(audio))
    video.write_videofile(output, fps=24)

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
    sleep(2)
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    sleep(5)
    
    # Upload
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(os.path.abspath(video_path))
    sleep(5)
    driver.find_element(By.ID, "textbox").send_keys(title)
    driver.find_element(By.ID, "next-button").click()
    driver.find_element(By.ID, "done-button").click()
    sleep(10)
    driver.quit()

if __name__ == "__main__":
    trends = get_trends()
    for idx, trend in enumerate(trends):
        script = generate_script(trend)
        create_audio(script, f"audio_{idx}.mp3")
        images = get_images(trend)
        make_video(images, f"audio_{idx}.mp3", f"video_{idx}.mp4")
        upload_to_yt(
            os.getenv('YT_EMAIL'),
            os.getenv('YT_PASSWORD'),
            f"video_{idx}.mp4",
            f"{trend} Trending Now!"
        )
