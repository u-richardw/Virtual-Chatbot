# Azure TTS Configuration
AZURE_API_KEY = "your-azure-api-key"  # Replace with your Azure API key
AZURE_REGION = "eastus"  # Replace with your Azure region
AZURE_TTS_URL = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
AZURE_VOICE = "en-US-AshleyNeural"  # Example voice (choose from Azure's voice list)

# Audio settings
SAMPLE_RATE = 22050  # Watson supports 22050 Hz

# Voice Activity Detection (VAD) settings
VAD_AGGRESSIVENESS = 2  # 0 = least aggressive, 3 = most aggressive

# Memory settings
MEMORY_LIMIT = 5
MEMORY_FILE = "tai_chan_memory.json"