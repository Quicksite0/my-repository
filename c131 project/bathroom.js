img = "";

function preload(){
    img = loadImage('bathroom.png');
}

function draw(){
    image(img, 0, 0, 450, 450);
}

function setup(){
    canvas = createCanvas(450, 450);
    canvas.center();
}
