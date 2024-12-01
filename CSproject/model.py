# Handles data and computation
#Includes logic for reading files, cleaning data, and calculating RT60

import numpy as np
import librosa
from scipy.signal import find_peaks

#load audio file and make sure it is in correct format
#converst MP3 to WAV if neccessary

def load_audio(file_path):
    try:
        #load file
        audio, sample_rate = librosa.load(file_path, sr=None, mono=True)
        return audio, sample_rate

    except Exception as e:
        print(f"Error loading audio: {e}")
        return None, None

#Clean audio and removing metadata

def clean_audio(audio):
    #librosa.load already handles mono
    return audio

