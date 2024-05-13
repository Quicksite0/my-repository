img = "";

function preload(){
    img = loadImage('lounge_room.png');
}

function draw(){
    image(img, 0, 0, 800, 420);
    fill("#FF0000");
    text("Television", 380, 70);
    noFill();
    stroke("#FF0000");
    rect(285, 80, 160, 85);
}

function setup(){
    canvas = createCanvas(640, 420);
    canvas.center();
}
