img = "";

function preload(){
    img = loadImage('laundry_room.png');
}

function draw(){
    image(img, 0, 10, 320, 500);
}

function setup(){
    canvas = createCanvas(320, 500);
    canvas.center();
}
