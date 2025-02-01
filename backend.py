import ollama
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from TTS.api import TTS
import time
import webrtcvad
import re

# Initialize Coqui TTS with Tacotron2
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

def get_ai_response(prompt):
    """Generate a response from Ollama (LLaMA 3)."""
    neuro_prompt = f"""
    You are Tai-Chan, an AI VTuber known for your deadpan humor, sarcasm, and chaotic energy.
    You often make dry jokes, pretend to misunderstand things for comedic effect, and occasionally troll the user.
    Stay playful, witty, and mischievous, but never be too aggressive.
    Keep responses short and snappy unless asked otherwise.

    User: {prompt}
    Tai-chan:
    """
    response = ollama.generate(model='llama3', prompt=neuro_prompt)
    return response['response']

def clean_text_for_tts(text):
    """Removes emojis and special characters that TTS can't process."""
    return re.sub(r'[^\w\s,.!?\'"-]', '', text)  # Keeps letters, numbers, punctuation

def ensure_min_length(text, min_chars=10):
    """Ensures the text is long enough for TTS by adding filler if needed."""
    if len(text) < min_chars:
        text += " ..."  # Add filler so TTS doesn't fail
    return text

def play_audio(text):
    """Convert text to speech using Coqui TTS and play it."""
    try:
        text = clean_text_for_tts(text)  # Remove emojis
        text = ensure_min_length(text)   # Ensure text is long enough
        audio = tts.tts(text=text)

        audio_np = np.array(audio, dtype=np.float32)
        audio_np /= np.max(np.abs(audio_np))  # Normalize to prevent clipping
        sd.play(audio_np, samplerate=22050)
        sd.wait()
    except Exception as e:
        print(f"Error in TTS: {e}")

# Initialize WebRTC VAD
vad = webrtcvad.Vad(2)  # Sensitivity (0 = least sensitive, 3 = most sensitive)

def is_speech(audio_data, sample_rate=16000, frame_duration=30):
    """Detects speech using WebRTC VAD before sending to SpeechRecognition."""
    frame_size = int(sample_rate * frame_duration / 1000)  # Convert ms to samples
    audio_np = np.frombuffer(audio_data, dtype=np.int16)

    for i in range(0, len(audio_np), frame_size):
        frame = audio_np[i:i+frame_size].tobytes()
        if vad.is_speech(frame, sample_rate):
            return True  # Speech detected
    return False  # No speech detected

def recognize_speech():
    """Always listens and only activates when speech is detected."""
    recognizer = sr.Recognizer()

    with sr.Microphone(sample_rate=16000) as source:
        print("Listening... Speak anytime.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Auto-adjust for noise

        while True:  # Infinite listening loop
            try:
                # Step 1: Passively listen for speech
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)  # Wait indefinitely
                
                # Step 2: Check if it's real speech using VAD
                if not is_speech(audio.frame_data, sample_rate=16000):
                    continue  # Ignore silence & background noise
                
                # Step 3: Recognize the speech
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text  # Return valid speech when detected

            except sr.UnknownValueError:
                print("Couldn't understand speech. Try again.")
            except sr.RequestError:
                print("SpeechRecognition error. Check your internet.")
                return None

def main():
    """Voice-based chat loop."""
    print("AI VTuber Backend - Voice Test")
    print("Say 'exit' to quit.\n")

    while True:
        user_input = recognize_speech()
        if user_input is None:
            continue  # If no valid input, ask again
        if user_input.lower() == "exit":
            break

        # Get AI response
        ai_response = get_ai_response(user_input)
        print(f"AI: {ai_response}")

        # Play audio
        play_audio(ai_response)

if __name__ == '__main__':
    main()
