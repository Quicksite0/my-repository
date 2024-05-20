img = "";

function preload(){
    img = loadImage('laundry_room.png');
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
    image(img, 0, 10, 320, 500);
}

function setup(){
    canvas = createCanvas(320, 500);
    canvas.center();

    objectDetector = ml5.objectDetector('cocossd', modelLoaded);
    document.getElementById("status").innerHTML = "Status : Detecting Objects";
}
