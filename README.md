# 🗣️ Text-to-Speech Web App (TTS Converter)

This is a Flask-based Text-to-Speech (TTS) web application that allows users to convert typed text into spoken audio. Users can choose from multiple voices (male/female) and languages, control speech speed, and download the audio as an `.mp4` file.

## 🔥 Features

- 🌍 **Multilingual Support**: Supports English (US, UK, Australia), French, Spanish, German, Italian, Japanese, and more.
- 👨‍🦱👩‍🦱 **Gender Selection**: Offers both male (via `pyttsx3`) and female (via `gTTS`) voice options.
- 🎚️ **Speed Control**: Adjust speaking speed using a slider.
- 💾 **Audio Download**: Converts TTS to `.mp4` format using `FFmpeg` and allows downloading.
- 📁 **Temporary File Management**: Uses UUIDs to generate unique filenames and deletes intermediate files to manage storage.



### 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/tts-web-app.git
cd tts-web-app




Install dependencies
**pip install -r requirements.txt**
USE PYTHON intrepreter
         **version 3.10.7 64bit**

Install FFmpeg
Windows: Download from https://ffmpeg.org/download.html, extract, and add to PATH.
macOS: brew install ffmpeg
Linux: sudo apt install ffmpeg


-Run the Application
Bash
**python app.py**



Open in Browser
Navigate to: http://127.0.0.1:5000/

Convert Text to Speech
Enter your text
Choose a voice and speed
Submit and download the .mp4 audio file


🛠️ Troubleshooting
--FFmpeg not found: Ensure ffmpeg is installed and added to your system PATH.
--No audio output: Check for missing voice engines or dependencies.
--PermissionError / FileNotFoundError: Ensure the static/audio directory exists and is writable.
