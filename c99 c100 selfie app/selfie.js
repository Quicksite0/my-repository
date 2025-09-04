var SpeechRecognition = window.webkitSpeechRecognition;

var recognition = new SpeechRecognition();

function start(){
    document.getElementById("textbox").innerHTML = "";
    recognition.start();
}

recognition.onresult = function(event){
    console.log(event);
    var Content = event.results[0][0].transcript;
    document.getElementById("textbox").innerHTML = "";
    console.log(Content);
    if(Content == "Take my selfie"){
        console.log("Taking Selfie ---")
        speak();
    }    
}

function speak(){
    var synth = window.speechSynthesis;
    speak_data = "Taking your selfie in five seconds";
    speak_data = document.getElementById("textbox").value;
    var utterThis = new SpeechSynthesisUtterance(speak_data);
    synth.speak(utterThis);
    Webcam.attach(camera)
    setTimeout(function(){
        take_snapshot();
        save();
        }, 5000);
}

Webcam.set({
    width:360,
    height:250,
    image_format:'png',
    png_quality:90
});
camera = document.getElementById("camera");

function take_snapshot{
    webcam.snap(function(data_url)){
        document.getElementById("result").innerHTML = '<img id="selfie_image" src="'+data_url+'">';
    }
}

function setTimeoutButton(){
    setTimeout(
        function(){
            alert("set Timeout Button");
        }, 3000);
}

function save(){
    link = document.getElementById("link");
    image = document.getElementById("selfie_image").src;
    link.href = image;
    link.click();
}