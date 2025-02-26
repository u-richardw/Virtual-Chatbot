from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import WATSON_API_KEY, WATSON_URL, WATSON_VOICE, SAMPLE_RATE
import sounddevice as sd
import numpy as np

# Initialize Watson TTS
authenticator = IAMAuthenticator(WATSON_API_KEY)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(WATSON_URL)

def play_audio(text):
    try:
        # Synthesize speech
        response = tts.synthesize(
            text=text,
            voice=WATSON_VOICE,
            accept="audio/wav"
        ).get_result()
        
        # Convert to numpy array
        audio_data = np.frombuffer(response.content, dtype=np.int16)
        audio_np = audio_data.astype(np.float32) / 32768.0  # Normalize
        
        # Play audio
        sd.play(audio_np, samplerate=SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(f"Watson TTS Error: {str(e)[:100]}")