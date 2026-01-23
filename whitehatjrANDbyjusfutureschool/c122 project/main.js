x = 0;
y = 0;

draw_apple = "";
screen_width = 0
screen_height = 0
apple = ""
to_number = ""




var SpeechRecognition = window.webkitSpeechRecognition;
  
var recognition = new SpeechRecognition();

function start()
{
  document.getElementById("status").innerHTML = "System is listening please speak";  
  recognition.start();
} 
 
recognition.onresult = function(event) {

 console.log(event); 

 content = event.results[0][0].transcript;

document.getElementById("status").innerHTML = "The speech has been recognized: " + content;

to_number = Number(content)

if(Number.isInteger(to_number)){
    document.getElementById("status").innerHTML = "Drawing Apple"
    draw_apple = "set"
}
}

function preload(){
    loadIMG = loadImage("https://i.ibb.co/VLCk4gr/apple.png")
    apple = loadIMG;
}

function setup(){

  screen_width = window.innerWidth;
  screen_width = window.innerHeight;

  canvas = createCanvas(screen_width, screen_height - 150);
  canvas.position(0,150);
}

function draw() {
  if(draw_apple == "set")
  {

    for (i = 1; i <= to_number; i++ ){
      x = Math.floor(Math.round(Math.random)* 700)
      y = Math.floor(Math.round(Math.random)* 400)

      image(apple,x,y,100,100)
    }

    document.getElementById("status").innerHTML = to_number + " Apples drawn";
    draw_apple = "";

    speak()
  }
}

function speak(){
    var synth = window.speechSynthesis;

    var utterThis = new SpeechSynthesisUtterance(speak_data);

    synth.speak(utterThis);

    speak_data = "";
}