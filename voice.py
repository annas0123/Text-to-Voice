from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import os
from gtts import gTTS
import tempfile
import uuid
from pydub import AudioSegment
import sys
import subprocess
import pyttsx3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Voice options
VOICE_OPTIONS = {
    'en-us-male': {'lang': 'en-us', 'engine': 'pyttsx3'},
    'en-uk-male': {'lang': 'en-uk', 'engine': 'pyttsx3'},
    # Female voices (using gTTS)
    'en-us-female': {'lang': 'en', 'tld': 'us', 'engine': 'gtts'},
    'en-uk-female': {'lang': 'en', 'tld': 'co.uk', 'engine': 'gtts'},
    'en-au-female': {'lang': 'en', 'tld': 'com.au', 'engine': 'gtts'},
    'fr-female': {'lang': 'fr', 'tld': 'fr', 'engine': 'gtts'},
    'es-female': {'lang': 'es', 'tld': 'es', 'engine': 'gtts'},
    'de-female': {'lang': 'de', 'tld': 'de', 'engine': 'gtts'},
    'it-female': {'lang': 'it', 'tld': 'it', 'engine': 'gtts'},
    'ja-female': {'lang': 'ja', 'tld': 'co.jp', 'engine': 'gtts'},
    # Male voices (using pyttsx3)
  
}

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible"""
    try:
        # Run ffmpeg version command to check if it's available
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def generate_tts_with_gtts(text, voice_settings, filepath, speed):
    """Generate TTS using gTTS"""
    tts = gTTS(text=text, lang=voice_settings['lang'], tld=voice_settings['tld'], slow=(speed < 1.0))
    tts.save(filepath)
    
    # Adjust speed if needed (speed > 1.0)
    if speed > 1.0:
        sound = AudioSegment.from_mp3(filepath)
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })
        sound_with_altered_frame_rate.export(filepath, format="mp3")

def generate_tts_with_pyttsx3(text, voice_settings, filepath, speed):
    """Generate TTS using pyttsx3 (for male voices)"""
    engine = pyttsx3.init()
    
    # Get all voices
    voices = engine.getProperty('voices')
    
    # Set male voice (usually index 0)
    if len(voices) > 0:
        engine.setProperty('voice', voices[0].id)  # Select first voice (usually male)
    
    # Set speaking rate (default is 200)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', int(rate * speed))
    
    # Save to temporary WAV file first
    temp_wav = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.wav")
    engine.save_to_file(text, temp_wav)
    engine.runAndWait()
    
    # Convert WAV to MP3
    sound = AudioSegment.from_wav(temp_wav)
    sound.export(filepath, format="mp3")
    
    # Remove temporary WAV file
    os.remove(temp_wav)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if ffmpeg is installed
        if not check_ffmpeg():
            return render_template('index.html', voices=VOICE_OPTIONS, 
                                  error="FFmpeg is not installed or not in PATH. Please install FFmpeg and try again.")
        
        # Get form data
        text = request.form.get('text', '')
        voice = request.form.get('voice', 'en-us-female')
        speed = float(request.form.get('speed', 1.0))
        
        if not text:
            return render_template('index.html', voices=VOICE_OPTIONS, error="Please enter some text")
        
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Get voice settings
            voice_settings = VOICE_OPTIONS.get(voice, VOICE_OPTIONS['en-us-female'])
            
            # Generate speech based on the engine
            if voice_settings.get('engine') == 'pyttsx3':
                generate_tts_with_pyttsx3(text, voice_settings, filepath, speed)
            else:
                generate_tts_with_gtts(text, voice_settings, filepath, speed)
            
            # Convert to MP4 
            mp4_filename = f"{uuid.uuid4()}.mp4"
            mp4_filepath = os.path.join(app.config['UPLOAD_FOLDER'], mp4_filename)
            
            sound = AudioSegment.from_mp3(filepath)
            sound.export(mp4_filepath, format="mp4")
            
            # Remove the temporary MP3 file
            os.remove(filepath)
            
            return redirect(url_for('download', filename=mp4_filename))
        except Exception as e:
            return render_template('index.html', voices=VOICE_OPTIONS, 
                                  error=f"An error occurred: {str(e)}. Please make sure FFmpeg is installed correctly.")
    
    return render_template('index.html', voices=VOICE_OPTIONS)

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('download.html', filename=filename)

@app.route('/get-file/<filename>')
def get_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
