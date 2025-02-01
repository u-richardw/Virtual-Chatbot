import elevenlabs
import sounddevice as sd
import numpy as np
# Set your API key
elevenlabs.api_key = "sk_1cd0acf5a65efb8d9d991bd70573c3a4c321dcbb2d94ddc8"
def play_audio(text):
    """Convert text to speech using ElevenLabs and play it."""
    try:
        # Specify the voice you want to use
        voice = "8bbJudyFc7qdK5dBOr6W"  # Replace with the desired voice name or ID

        # Generate the audio using ElevenLabs
        audio = elevenlabs.generate(text=text, voice=voice)

        # Convert the audio to NumPy format (if needed for playback)
        audio_np = np.array(audio, dtype=np.float32)

        # Normalize and play the audio
        audio_np /= np.max(np.abs(audio_np))  # Normalize audio to avoid clipping
        sd.play(audio_np, samplerate=22050)
        sd.wait()

    except Exception as e:
        print(f"Error in TTS: {e}")

# Test the function with a sample text
play_audio("Hello, this is Tai-chan!")