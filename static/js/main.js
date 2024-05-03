var socket = io.connect('http://localhost:5000');
var recognition = new webkitSpeechRecognition();
var transcript;
//recognition.continuous = false;
//recognition.interimResults = false;
recognition.lang = 'en-US';

// Starting the microphone when the button is clicked
document.getElementById('start-microphone-button').addEventListener('click', function() {
    recognition.start();
});

// Displaying the transcript in the transcription textbox
recognition.onresult = function(event) {
    transcript = event.results[event.results.length - 1][0].transcript;
    document.getElementById('transcription-textbox').value = transcript;
    
};

// Sending the transcript to the python script when the speech ends
recognition.onspeechend = function () {
    socket.emit('/message', { 'text': transcript });
    recognition.stop();
}

// display the answer of the llm in the answer textbox
socket.on('answer', function(data) {
    document.getElementById('answer-textbox').value = data.text;
    
});


// Displaying the image in the image container
socket.on('image_data', function(data) {
    let imageContainer = document.getElementById('image-container');

    // Check if an image already exists
    let existingImage = imageContainer.querySelector('img');
    if (existingImage) {
        // If an image exists, remove it
        imageContainer.removeChild(existingImage);
    }

    // Create a new image element
    let imgElement = document.createElement('img');

    // Decode the base64 image and display it in the image element
    imgElement.src = 'data:image/png;base64,' + data.image;

    // Append the new image element to the div
    imageContainer.appendChild(imgElement);
});