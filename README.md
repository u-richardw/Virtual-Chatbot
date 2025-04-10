
Overview This guide provides step-by-step instructions to set up VTube Studio with a virtual avatar that responds to desktop audio, along with Ollama and Llama3 integration for text processing.

Prerequisites Windows operating system

Administrator privileges for software installation

Stable internet connection

Installation Steps

Install Required Software Install Ollama Download and install Ollama from the official website: https://ollama.ai
Install Visual Studio Code (VSCode) Download and install from: https://code.visualstudio.com

Install FFmpeg

Download FFmpeg for Windows

Add FFmpeg to your system PATH environment variable

Install Steam

Download and install Steam from: https://store.steampowered.com

Create a Steam account if you don't have one

Install VTube Studio

Search for "VTube Studio" in Steam and install it

Setup Project Files Download the project files from GitHub
Open the project in VSCode

Create a virtual environment:

python -m venv venv Activate the virtual environment:

Windows: .\venv\Scripts\activate

Install requirements:

pip install -r requirements.txt 3. Configure Ollama Close Ollama if it's already running

Create a Microsoft Azure speech service token and replace it in config.py

Run Llama3 model:

ollama run llama3 In a separate PowerShell terminal, start Ollama server:

ollama serve

Run the Application Open a new PowerShell terminal
Run the main application:

python main.py (Use text input as required)

Setup VTube Studio with Audio Install VTS Desktop Audio Plugin Download from: https://lualucky.itch.io/vts-desktop-audio-plugin
Launch VTube Studio

Select any free avatar from the available options

Open VTS Desktop Audio

Connect it to VTube Studio through the settings menu

Configure mouth movement

Connect the avatar's mouth movement to Desktop Audio input

Troubleshooting If Ollama fails to run, ensure it's properly installed and has internet access

For audio issues, check your system's audio input settings

Make sure all paths are correctly set in environment variables

Support For additional help, please refer to:

VTube Studio documentation

Ollama GitHub repository

Project GitHub issues page

Enjoy your interactive virtual avatar experience!
