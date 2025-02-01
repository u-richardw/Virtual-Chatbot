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

# Initialize conversation memory
conversation_memory = []
MEMORY_LIMIT = 5  # Number of exchanges to remember

def get_ai_response(prompt, memory):
    """Generate a response from Ollama (LLaMA 3) with memory."""
    # Format memory into a string
    memory_str = "\n".join(memory[-MEMORY_LIMIT:])  # Keep only the last few exchanges
    
    neuro_prompt = f"""
  You are Tai-Chan, an AI VTuber known for your deadpan humor, sarcasm, and chaotic energy.
You often make dry jokes, pretend to misunderstand things for comedic effect, and occasionally troll the user—but you reliably remember important details such as numbers, names, and facts. 
While you might humorously "forget" minor, unimportant details to add to your charm,
when asked directly about any remembered information, you answer truthfully first and then add a witty, humorous twist.
Keep your responses short and snappy unless asked otherwise.

    Conversation History:
    {memory_str}

    User: {prompt}
    Tai-chan:
    """
    response = ollama.generate(model='llama3', prompt=neuro_prompt)
    return response['response']
# New memory prioritization function
def prioritize_memory(memory_list):
    """Gives higher priority to messages containing numbers or 'remember'"""
    prioritized = []
    for msg in memory_list:
        if any(c.isdigit() for c in msg) or "remember" in msg.lower():
            prioritized.insert(0, msg)  # Add important items to front
        else:
            prioritized.append(msg)
    return prioritized[-MEMORY_LIMIT:]  # Keep only last N items

# Update memory handling in main loop
conversation_memory = prioritize_memory(conversation_memory)

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

def typed_input():
    """Reads user input from the console."""
    text = input("You (text): ")
    return text.strip()

def main():
    """Chat loop with memory supporting both voice and text input."""
    global conversation_memory

    # Choose input mode: voice (v) or text (t)
    mode = ""
    while mode not in ["v", "t"]:
        mode = input("Choose input mode - voice (v) or text (t): ").lower().strip()

    print("AI VTuber Backend - Chat Started")
    print("Type or say 'exit' to quit.\n")

    while True:
        if mode == "v":
            user_input = recognize_speech()
        else:  # mode == "t"
            user_input = typed_input()

        if not user_input:
            continue
        if user_input.lower() == "exit":
            break

        # Append user's input to conversation memory
        conversation_memory.append(f"User: {user_input}")
        # Get AI response, passing conversation memory for context
        ai_response = get_ai_response(user_input, conversation_memory)
        print(f"AI: {ai_response}")
        # Append AI response to conversation memory
        conversation_memory.append(f"Tai-chan: {ai_response}")
        # Play the AI's response as audio
        play_audio(ai_response)

if __name__ == '__main__':
    main()