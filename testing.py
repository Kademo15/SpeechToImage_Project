# %%
# Import the OpenAI library. This library provides a Python interface to the OpenAI API.
from openai import OpenAI
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json


# Set the sample rate and the number of channels
sample_rate = 16000
channels = 1

# Load the model
model = Model("models/vosk-model-en-us-0.22")

# Create a recognizer
rec = KaldiRecognizer(model, sample_rate)

# Define a callback function to process the audio chunks
def callback(indata, frames, time, status):
    if rec.AcceptWaveform(indata.flatten().tobytes()):
        result = rec.Result()
        result = json.loads(result)
        if result.get('text'):  # Only print when there is text
            print("Transcription: ", result['text'])

# Create a stream to record audio
stream = sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate, dtype='int16')

# Start recording and processing
with stream:
    print("Recording and transcribing. Press Ctrl+C to stop.")
    while True:
        sd.sleep(200)




