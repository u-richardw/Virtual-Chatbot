import os
import requests

# Replace with your Azure API key and region
subscription_key = "2mRWDsWWjm5q0GdKXSATspDUMKalYq8shduhuBUUUORO71mF1NQNJQQJ99BBACYeBjFXJ3w3AAAYACOGlcBk"
region = "eastus"  # e.g., "eastus"

# API endpoint
url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"

# Headers
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
}

# SSML for the text with Ashley's voice and increased pitch
body = f"""
<speak version='1.0' xml:lang='en-US'>
    <voice name='en-US-AshleyNeural'>
        <prosody pitch="+10%">
            She sells seashells by the seashore
        </prosody>
    </voice>
</speak>
"""

# Make the API request
response = requests.post(url, headers=headers, data=body)

# Save the audio to a file
if response.status_code == 200:
    with open("ashley_pitched_up.mp3", "wb") as f:
        f.write(response.content)
    print("Audio saved as ashley_pitched_up.mp3")
else:
    print("Error:", response.status_code, response.text)