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
````.\venv\Scripts\activate```` on windows or ````source venv/bin/activate```` on linux

Install the needed requirements via 
````pip install -r requirements.txt````

### Setup and usage
Before launching the program open LM studio, download a model you like, go to the server tab inside of LM studio and start the server. 

Furthermore ComfyUI needs to be running in order for SpeechToImage to work. Please refer to comfyUI documentation listed in the Dependencies part of this documentation to get ComfyUI up and running.

Once both dependencies are running, we can launch the application still with an activated venv via ````python main.py````.

DO NOT click on the url that will show up in the terminal, instead open chrome and open the url ````localhost:5000````.

Click the record button to start talking and wait for the image to be generated, 
in the first text box you will see what the speech recognition understood you said 
and in the second text box you will see the improved prompt the llm came up with. 
If you want to see how long the generation is taking you can open the terminal that comfyUI is running
and should find a progress bar.

## Documentation

### Project idea
I started being interested in ai image generation tools over the last few months because i was fascinated by what it could create and how it works. I saw what chatGPT did with bing ai where you write an llm that then talks to the image generation ai in order to create your image. I wanted to take that a step further so for my project i wanted the user to be able to just say what comes to his mind and both ai's would work together to create a beautiful image.

### Technologies used / stack
Python an javascript was used to create this project. I used ComfyUI and LM Studio, ComfyUI a tool to generate images and LM Studio a tool to run llm's, both feature an api to make interaction easier. The python packages for this project can be found in the requirements.txt file, the main package was vlask, a package to easily create a userface that reacts with python code. 

### Conclusion
My project does work and I managed to complete it in time. I had some issues with the interaction between the javascript side and the python side

## Lessons learned
At first I had a lot of setbacks. 

I tried to have local model running in order to transcribe what the users said but that caused some issues, half of the time it wasnt working it took quite some GB on the users machine and it ran very poorly on weak hardeware. To fix that issue I switched to the google speech recognition api integrated into google chrome. 

I tried to use python only but very quickly found out that it would make it way easier to combine it with javascript, because the communication between my code and the ComfyUI api worked via websockets, furthermore i needed to use javascript anyway to use the google speech api. 

I also took some time to figure out how the ComfyUI api should be called to interact with it. 

I overcame those problems and now know much better how to handle apis. 

I also learned some python and a bit of javascript.

I have a better understanding how web user interfaces communicate with the code underneath. 

I also learned a bit about llm's (giving the model context, system and user prompts)

### Next steps
I could improve the project by giving more user options such as a way to upload a custom workflow or being able to change the model or settings. 

I could use [llama.cpp](https://github.com/ggerganov/llama.cpp) and download it automatically inside the project so that the user doesnt have to mess with downloading LM Studio.

### References
https://github.com/comfyanonymous/ComfyUI/tree/master/script_examples

https://www.google.com/intl/en/chrome/demos/speech.html

https://lmstudio.ai/

https://github.com/features/copilot

https://flask.palletsprojects.com/en/3.0.x/#
