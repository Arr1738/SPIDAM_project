# Handles data and computation
#Includes logic for reading files, cleaning data, and calculating RT60

import numpy as np
import librosa
from pydub import AudioSegment
import os


#load audio file and make sure it is in correct format
#converst MP3 to WAV if necessary

def convert_to_wav(file_path):
    if file_path.endswith('.wav'):
        return file_path

    #load audio file using pydub
    audio = AudioSegment.from_file(file_path)

    #save as new .wav file
    wav_path = os.path.splitext(file_path)[0] + '.wav'
    audio.export(wav_path, format="wav")
    print(f"Converted {file_path} to {wav_path}")
    return wav_path

def load_audio(file_path):
    try:
        #convert to wav if necessary
        wav_path = convert_to_wav(file_path)

        #load file
        audio, sample_rate = librosa.load(file_path, sr=None, mono=True)
        print(f"Loaded file: {wav_path}")

        #clean temp wav file if converted
        if not file_path.endswith('.wav'):
            os.remove(wav_path)
            print(f"Temporary file {wav_path} removed.")
        return audio, sample_rate

    except Exception as e:
        print(f"Error loading audio: {e}")
        return None, None

#Clean audio and removing metadata

def clean_audio(audio):
    #librosa.load already handles mono
    return audio

#calculate RT60 value for audio data

def calculate_rt60(audio, sample_rate):
    #energy decay curve
    squared_signal = audio ** 2
    decay_curve = np.cumsum(squared_signal[::-1])[::-1]

    epsilon = 1e-10
    decay_curve += epsilon #prevents division by zero

    #convert to decibels
    decay_db = 10 * np.log10(decay_curve / np.max(decay_curve))

    #find when decay curve reaches -60 dB
    time_axis = np.linspace(0, len(audio) / sample_rate, len(decay_db))

    rt60_index = np.where(decay_db <= -60)[0]

    if rt60_index.size > 0:
        rt60_time = time_axis[rt60_index[0]]
        print(f"RT60 time: {rt60_time}")
        return rt60_time
    else:
        print("RT60 calculation could not find a valid decay point")
        return None

#test
if __name__ == '__main__':
    file_path =  "16bit1chan.wav"
    audio, sr = load_audio(file_path)
    if audio is not None:
        print(f"Sample Rate: {sr}")
        rt60 = calculate_rt60(audio, sr)
        if rt60:
            print(f"RT60: {rt60:.2} seconds")
        else:
            print("RT60 calculation failed")
