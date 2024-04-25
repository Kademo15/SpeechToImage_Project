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