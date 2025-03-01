import requests
import numpy as np
import sounddevice as sd
from config import AZURE_API_KEY, AZURE_REGION, AZURE_TTS_URL, AZURE_VOICE, SAMPLE_RATE

# Headers for Azure TTS API
AZURE_HEADERS = {
    "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
    "Content-Type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
}

def play_audio(text, save_to_file=None):
    try:
        # SSML for the text with the specified voice
        body = f"""
        <speak version='1.0' xml:lang='en-US'>
            <voice name='{AZURE_VOICE}'>
                {text}
            </voice>
        </speak>
        """

        # Make the API request
        response = requests.post(AZURE_TTS_URL, headers=AZURE_HEADERS, data=body)

        # Check for errors
        if response.status_code != 200:
            print(f"Azure TTS Error: {response.status_code}, {response.text}")
            return

        # Convert to numpy array
        audio_data = np.frombuffer(response.content, dtype=np.int16)
        audio_np = audio_data.astype(np.float32) / 32768.0  # Normalize

        # Play audio
        sd.play(audio_np, samplerate=SAMPLE_RATE)
        sd.wait()

        # Save audio to file if requested
        if save_to_file:
            with open(save_to_file, "wb") as f:
                f.write(response.content)
            print(f"Audio saved to {save_to_file}")
    except Exception as e:
        print(f"Azure TTS Error: {str(e)[:100]}")