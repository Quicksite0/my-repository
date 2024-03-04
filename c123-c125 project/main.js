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

leftWristX=0;
rightWristX=0;
difference=0;

function gotPoses(results){
    if(results.length > 0){
        leftWristX = results[0].pose.leftWrist.x;
        rightWristX = results[0].pose.rightWrist.x;
        difference = floor(leftWristX - rightWristX);
        console.log(results);
    }
}

function draw(){
    background('lime');
    textSize(difference);
    fill('aqua');
    stroke('aqua')
    text('Alessandro', 100, 100);
}