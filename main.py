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

                          
