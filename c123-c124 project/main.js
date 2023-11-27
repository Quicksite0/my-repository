function setup(){
    video = createCapture(VIDEO);
    video.size(500, 500);
    video.position(50);

    canvas = createCanvas(550, 550);
    canvas.position(650, 90);
    poseNet = ml5.poseNet(video, modelLoaded);
    poseNet.on('pose', gotPoses);
}

function modelLoaded(){
    console.log('PoseNet is Initialised');
}

function gotPoses(results){
    if(results.length > 0){
        console.log(results);
    }
}

function draw(){
    background('#00FF00');
}
