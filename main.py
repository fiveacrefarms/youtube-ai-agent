import os
from pytrends.request import TrendReq
from gtts import gTTS
import requests
pytrends = TrendReq()
trends = pytrends.trending_searches() .head(3) .tolist()
topic = trends[0]
script_response = requests.post("https://api-interference.huggingface.co/models/gpt4"
                                headers={Authorization": f"Bearer{os.environ[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]}"}
                                json={"inputs": f"Write a YouTube script about {topic}."})
                                script = script_response.json()[0]['generated_text']
                                tts = gTTS(text=script, lang='en')
                                tts.save("voiceover.mp3")
                                print(f"Video script for '{topic}'generated!")
unsplash_response = requests.get (

f"https://api.unsplash.com/photos /

random?query={topic}

&client_id={os.environ['vfUMEhRUm7L1ntTh8scCNFuJiOaYDzKxVfUNHv0t_Jw']

}"

image_url = unsplash_response.json ()

["urls" ]["regular"]

image_data =

requests. get (image_url) .content with open ("background.jpg", "wb") as f:

f.write(image_data)



os. system 'ffmpeg -loop 1 -i

background.jpg -i voiceover.mp3 -c:v libx264 -t 30 -pix_fmt yuv420p

output. mp4 ')
                          
