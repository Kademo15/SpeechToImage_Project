# %%
# Import the OpenAI library. This library provides a Python interface to the OpenAI API.
import random
from openai import OpenAI
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import uuid
import json
import urllib.request
import urllib.parse
import websocket
import base64


#Setup flask and socketio
app = Flask(__name__)
socketio = SocketIO(app)
server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


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
    call_ComfyUI(completion.choices[0].message.content)








def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images









def call_ComfyUI(new_prompt):
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
                "seed": 8596257,
                "steps": 30
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "dreamshaper_8.safetensors"
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": 768,
                "width": 768
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
    prompt["6"]["inputs"]["text"] = new_prompt

    prompt["3"]["inputs"]["seed"] = random.randint(1000000, 9999999)


    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, prompt)

    #Commented out code to display the output images:

    for node_id in images:
        for image_data in images[node_id]:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            socketio.emit('image_data', {'image': base64_image})
            print("Image data sent")
            # Now, send base64_image to your JavaScript code


if __name__ == '__main__':
    # Use app.run() instead of socketio.run() when running in a Jupyter notebook
    socketio.run(app, debug=True, use_reloader=False)
    #app.run(debug=True)










# %%
