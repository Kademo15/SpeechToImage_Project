# SpeechToImage documentation
This is a school project from a student of the Lycée des Arts et Métiers
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
````.\venv\Scripts\activate```` on windows or ````source venv/bin/activate```` on linux

Install the needed requirements via 
````pip install -r requirements.txt````

### Setup and usage
Before launching the program open LM studio, download a model you like, go to the server tab inside of LM studio and start the server. 

Furthermore ComfyUI needs to be running in order for SpeechToImage to work. Please refer to comfyUI documentation listed in the Dependencies part of this documentation to get ComfyUI up and running.

Once both dependencies are running, we can launch the application still with an activated venv via
````python main.py````

DO NOT click on the url that will show up in the terminal, instead open chrome and open the url ````localhost:5000````

Click the record button to start talking and wait for the image to be generated, 
in the first text box you will see what the speech recognition understood you said 
and in the second text box you will see the improved prompt the llm came up with. 
If you want to see how long the generation is taking you can open the terminal that comfyUI is running
and should find a progress bar. 
