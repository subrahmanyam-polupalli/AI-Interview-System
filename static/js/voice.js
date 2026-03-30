function speak(text){

const speech = new SpeechSynthesisUtterance();

speech.text = text;
speech.lang = "en-US";

startTalking();

speech.onend = function(){
stopTalking();
};

speechSynthesis.cancel();
speechSynthesis.speak(speech);

}

function startVoiceInput(){

const recognition = new webkitSpeechRecognition();

recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

recognition.start();

recognition.onresult = function(event){

const text = event.results[0][0].transcript;

document.getElementById("answerBox").value = text;

};

recognition.onerror = function(){
alert("Voice not detected. Please try again.");
};

}