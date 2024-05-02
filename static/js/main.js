var socket = io.connect('http://localhost:5000');
var recognition = new webkitSpeechRecognition();
var transcript;
//recognition.continuous = false;
//recognition.interimResults = false;
recognition.lang = 'en-US';

document.getElementById('start-microphone-button').addEventListener('click', function() {
    recognition.start();
});

recognition.onresult = function(event) {
    transcript = event.results[event.results.length - 1][0].transcript;
    document.getElementById('transcription-textbox').value = transcript;
    
};

recognition.onspeechend = function () {
    //action.innerHTML = "<small>stopped listening, hope you are done...</small>";
    socket.emit('/message', { 'text': transcript });
    recognition.stop();
}

socket.on('answer', function(data) {
    document.getElementById('answer-textbox').value = data.text;
    
});

socket.on('image_data', function(data) {
    // Get the div with id 'image-container'
    let imageContainer = document.getElementById('image-container');

    // Check if an image already exists
    let existingImage = imageContainer.querySelector('img');
    if (existingImage) {
        // If an image exists, remove it
        imageContainer.removeChild(existingImage);
    }

    // Create a new image element
    let imgElement = document.createElement('img');

    // Set the source of the image element to the Base64 image data
    imgElement.src = 'data:image/png;base64,' + data.image;

    // Append the new image element to the div
    imageContainer.appendChild(imgElement);
});