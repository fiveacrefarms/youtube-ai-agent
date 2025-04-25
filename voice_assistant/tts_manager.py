
from TTS.api import TTS

class TTSManager:
    def __init__(self):
        # Load TTS model
        self.tts = TTS(model_name="tts_models/en/ljspeech/vits", gpu=False)

    def text_to_speech(self, text, output_file="output.wav"):
        # Generate speech and save to file
        self.tts.tts_to_file(text=text, file_path=output_file)
        return output_file
