from memory import load_memory, save_memory
from ai_handler import get_ai_response
from speech_input import recognize_speech, typed_input
from audio import play_audio

def main():
    conversation_memory = load_memory()
    
    mode = ""
    while mode not in ["v", "t"]:
        mode = input("Choose input mode - voice (v) or text (t): ").lower().strip()
    
    print("AI VTuber Backend - Chat Started")
    print("Type or say 'exit' to quit.\n")

    try:
        while True:
            user_input = recognize_speech() if mode == "v" else typed_input()
            
            if not user_input:
                continue
            if user_input.lower() == "exit":
                break

            conversation_memory.append(f"User: {user_input}")
            ai_response = get_ai_response(user_input, conversation_memory)
            print(f"AI: {ai_response}")
            conversation_memory.append(f"Tai-chan: {ai_response}")
            play_audio(ai_response)
            
    finally:
        save_memory(conversation_memory)
        print("\nMemory saved for next session!")

if __name__ == '__main__':
    main()