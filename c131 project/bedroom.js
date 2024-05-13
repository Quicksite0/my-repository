img = "";

function preload(){
    img = loadImage('bedroom.png');
}

function draw(){
    image(img, 0, 0, 800, 420);
}

function setup(){
    canvas = createCanvas(640, 420);
    canvas.center();
}
