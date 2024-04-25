# %%
# Import the OpenAI library. This library provides a Python interface to the OpenAI API.
from openai import OpenAI
import sounddevice as sd
import numpy as np
import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import socket


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


@socketio.on('/message')
def handle_message(data):
    print("Message received")
    history.append({"role": "user", "content": data['text']})
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=history,
        temperature=0.7,
    )
    print("Ai response: ", completion.choices[0].message.content)
    history.append({"role": "assistant", "content": completion.choices[0].message.content})
    emit('answer', {'text': completion.choices[0].message.content})
    preparePromptAndRequest(completion.choices[0].message.content)

def requestComfyUi(llmPrompt):
    p = {"prompt": llmPrompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

def preparePromptAndRequest(prompt):
    
    prompt_text = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 8,
            "denoise": 1,
            "latent_image": [
                "5",
                0
            ],
            "model": [
                "4",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "sampler_name": "euler",
            "scheduler": "normal",
            "seed": 8566257,
            "steps": 20
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "v1-5-pruned-emaonly.ckpt"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "batch_size": 1,
            "height": 512,
            "width": 512
        }
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "masterpiece best quality girl"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "bad hands"
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        }
    }
}
"""

    prompt = json.loads(prompt_text)
    #set the text prompt for our positive CLIPTextEncode
    prompt["6"]["inputs"]["text"] = prompt


    requestComfyUi(prompt)

if __name__ == '__main__':
    # Use app.run() instead of socketio.run() when running in a Jupyter notebook
    socketio.run(app, debug=True, use_reloader=False)

# %%
