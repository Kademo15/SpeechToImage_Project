# %%
# Import the OpenAI library. This library provides a Python interface to the OpenAI API.
from openai import OpenAI
import sounddevice as sd
import numpy as np
import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit


#Setup flask and socketio
app = Flask(__name__)
socketio = SocketIO(app)


# Create an instance of the OpenAI client. The base_url parameter is set to a local server and the api_key is not needed in this case.
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Define a global variable to keep track of the recording state
global history

# Define the conversation history
history = [
    {"role": "system", "content": "I'm going to give you an image idea and you are going to return me a creative and enhanced description with keywords of the image you imagine. The description should not be longer than 30 words and be specific and discriptive. Dont be afraid to be creative"},
]

@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    history.append({"role": "user", "content": data['text']})
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=history,
        temperature=0.7,
    )
    history.append({"role": "assistant", "content": completion.choices[0].message['content']})
    emit('answer', {'text': completion.choices[0].message['content']})

if __name__ == '__main__':
    # Use app.run() instead of socketio.run() when running in a Jupyter notebook
    socketio.run(app, debug=True, use_reloader=False)

# %%
