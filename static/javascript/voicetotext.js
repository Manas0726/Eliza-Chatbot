let recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'en-US';

let inputFieldV = document.getElementById('textInput');

let micOn = document.getElementById('micOn');
let micOff = document.getElementById('mic');

micOn.addEventListener('click', () => {
  micOn.style.display = 'none';
  micOff.style.display = 'flex';

  recognition.stop();
});

micOff.addEventListener('click', () => {
  micOn.style.display = 'flex';
  micOff.style.display = 'none';
  recognition.start();
});

recognition.onstart = function() {
  console.log('Voice recognition activated. Try speaking into the microphone.');
};

recognition.onend = function() {
  console.log('Voice recognition turned off.');
};

recognition.onerror = function(event) {
  console.error(event.error);
};

recognition.onresult = function(event) {
  let finalTranscript = '';
  for (let i = event.resultIndex; i < event.results.length; i++) {
    let transcript = event.results[i][0].transcript;
    if (event.results[i].isFinal) {
      finalTranscript += transcript;
    }
  }
  inputFieldV.value = finalTranscript;
};
