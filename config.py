# Configuration constants


WATSON_API_KEY = "jzKz0DN5N3dgIAXkOTAn1FOKy5eKSKnfsma_nKT4FkMB"
WATSON_URL = "https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/4b33fc84-bdb3-4588-8b1c-c9e8b57f2f35"
# Voice options (choose one)
WATSON_VOICE = "en-US_AllisonV3Voice"  # Female, expressive
# WATSON_VOICE = "en-US_MichaelV3Voice"  # Male, clear

# Audio settings
SAMPLE_RATE = 22050  # Watson supports 22050 Hz

# Voice Activity Detection (VAD) settings
VAD_AGGRESSIVENESS = 2  # 0 = least aggressive, 3 = most aggressive

# Memory settings
MEMORY_LIMIT = 5
MEMORY_FILE = "tai_chan_memory.json"