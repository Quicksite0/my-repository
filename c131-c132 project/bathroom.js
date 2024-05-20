img = "";

function preload(){
    img = loadImage('bathroom.png');
}

function modelLoaded(){
    console.log("Model Loaded!");
    Status = true;
    objectDetector.detect(img, gotResult);
}

function gotResult(error, results){
    if(error){
        console.log(error);
    }
    console.log(results);
}

function draw(){
    image(img, 0, 0, 450, 450);
}

function setup(){
    canvas = createCanvas(450, 450);
    canvas.center();

    objectDetector = ml5.objectDetector('cocossd', modelLoaded);
    document.getElementById("status").innerHTML = "Status : Detecting Objects";
}

