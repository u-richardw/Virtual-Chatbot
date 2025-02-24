import speech_recognition as sr
import webrtcvad
import numpy as np
from config import VAD_AGGRESSIVENESS, SAMPLE_RATE

vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

def is_speech(audio_data, sample_rate=16000, frame_duration=30):
    frame_size = int(sample_rate * frame_duration / 1000)
    
    # Convert audio data to 16-bit PCM format
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    
    # Process in chunks that match WebRTC VAD requirements
    for i in range(0, len(audio_np), frame_size):
        frame = audio_np[i:i+frame_size]
        if len(frame) < frame_size:
            continue  # Skip incomplete frames
        try:
            if vad.is_speech(frame.tobytes(), sample_rate):
                return True
        except:
            return False
    return False

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone(sample_rate=SAMPLE_RATE) as source:
        print("Listening... Speak anytime.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                if not is_speech(audio.frame_data, sample_rate=SAMPLE_RATE):
                    continue
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Couldn't understand speech. Try again.")
            except sr.RequestError:
                print("SpeechRecognition error. Check your internet.")
                return None

def typed_input():
    return input("You (text): ").strip()