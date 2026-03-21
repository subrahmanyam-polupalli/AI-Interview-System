
let recognition = null;
let isRecording = false;

function getMicButton(){
    return document.getElementById("micButton");
}

function updateMicState(active){
    const btn = getMicButton();
    const status = document.getElementById("voiceStatus");
    if(!btn) return;

    if(active){
        btn.classList.add("active");
        btn.title = "Listening...";
        if(status) status.textContent = "Listening... speak your answer now.";
    } else {
        btn.classList.remove("active");
        btn.title = "Click to speak";
        if(status) status.textContent = "Click the microphone to record your answer.";
    }
}

function startVoice(){
    if(!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)){
        alert("Voice recognition is not supported in this browser.");
        return;
    }

    if(isRecording){
        stopVoice();
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function(){
        isRecording = true;
        updateMicState(true);
    };

    recognition.onresult = function(event){
        const transcript = event.results[0][0].transcript;
        const answerBox = document.getElementById("answerBox");
        if(answerBox){
            answerBox.value = transcript;
        }
    };

    recognition.onerror = function(){
        isRecording = false;
        updateMicState(false);
    };

    recognition.onend = function(){
        isRecording = false;
        updateMicState(false);
    };

    recognition.start();
}

function stopVoice(){
    if(recognition){
        recognition.stop();
    }
    isRecording = false;
    updateMicState(false);
}
