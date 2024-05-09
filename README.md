# SpeechToImage documentation
This is a school project from a student of the Lycée des Arts et Métiers (from scratch)
## Installation
### Dependencies
The chrome browser

This project implements two already existing projects [ComfyUI](https://github.com/comfyanonymous/ComfyUI) and [LM studio](https://lmstudio.ai/). 

Please refer to their specific documentation to correctly install these two first before installing SpeechToImage_Project.

### Prerequisites
Python, git

### Install
Open your terminal and git clone this repo via 

````git clone https://github.com/Kademo15/SpeechToImage_Project````

Create a venv ````python -m venv venv````

Activate that venv you just created with
````.\venv\Scripts\activate```` on windows or ````source venv/bin/activate```` on Linux

Install the needed requirements via 
````pip install -r requirements.txt````

### Setup and usage
Before launching the program open LM Studio, download a model you like, go to the server tab inside of LM Studio, and start the server. 

Furthermore, ComfyUI needs to be running for SpeechToImage to work. Please refer to the ComfyUI documentation listed in the Dependencies part of this documentation to get ComfyUI up and running. Finally you will need to download [this](https://civitai.com/api/download/models/128713) 
specific model and put it in your ComfyUI folder under ````checkpoints```` for it to function. 

Once both dependencies are running, we can launch the application still with an activated venv via ````python main.py````.

DO NOT click on the URL if it shows up in the terminal, instead open Chrome and open the URL ````localhost:5000````.

Click the record button to start talking and wait for the image to be generated, 
in the first text box, you will see what the speech recognition understood you said 
and in the second text box, you will see the improved prompt the LLM came up with. 
If you want to see how long the generation is taking you can open the terminal that comfyUI is running
and should find a progress bar.

## Documentation

### Project idea
I started being interested in AI image generation tools over the last few months because I was fascinated by what they could create and how they work. I saw what chatGPT did with Bing AI where you write an LLM that then talks to the image generation AI to create your image. I wanted to take that a step further so for my project I wanted the user to be able to just say what comes to his mind and both AIs would work together to create a beautiful image.

### Technologies used / stack
Python and JavaScript were used to create this project. I used ComfyUI and LM Studio, ComfyUI a tool to generate images, and LM Studio a tool to run LLMs, both feature an API to make interaction easier. The Python packages for this project can be found in the requirements.txt file, the main package was Flask, a package to easily create a user interface that reacts with Python code. 

### Conclusion
My project does work and I managed to complete it in time. I had some issues with the interaction between the javascript side and the Python side. A lot of it is hardcoded but that's for future versions to improve on

## Lessons learned
At first, I had a lot of setbacks. 

I tried to have a local model running to transcribe what the users said but that caused some issues, half of the time it wasn't working, took quite some GB on the user's machine and it ran very poorly on weak hardware. To fix that issue I switched to the Google Speech recognition API integrated into Google Chrome. 

I tried to use Python only but very quickly found out that it would make it way easier to combine it with javascript because the communication between my code and the ComfyUI API worked via WebSockets, furthermore, I needed to use javascript anyway to use the google speech API. 

I also took some time to figure out how the ComfyUI API should be called to interact with it. 

I overcame those problems and now know much better how to handle APIs. 

I also learned some Python and a bit of JavaScript.

I have a better understanding of how web user interfaces communicate with the code underneath. 

I also learned a bit about LLM's (giving the model context, system, and user prompts)

### Next steps
I could improve the project by giving more user options such as a way to upload a custom workflow or being able to change the model or settings. 

I could use [llama.cpp](https://github.com/ggerganov/llama.cpp) and download it automatically inside the project so that the user doesn't have to mess with downloading LM Studio.

### References
https://github.com/comfyanonymous/ComfyUI/tree/master/script_examples

https://www.google.com/intl/en/chrome/demos/speech.html

https://lmstudio.ai/

https://github.com/features/copilot

https://flask.palletsprojects.com/en/3.0.x/#
