song_1 ="";
song_2 ="";
leftWristX = 0;
leftWristY = 0;
rightWristX = 0;
rightWristY = 0;
scoreLeftWrist = 0;
scoreRightWrist = 0;
songStatusLeft = "";
songStatusRight = "";

function preload(){
    song_1 = loadSound("song_1.mp3");
    song_2 = loadSound("song_2.mp3");
}

function setup(){
    canvas = createCanvas(600, 500);
    canvas.center();

    video = createCapture(VIDEO);
    video.hide();

    poseNet = ml5.poseNet(video, modelLoaded);
    poseNet.on('pose', gotPoses);
}

function draw(){
    image(video, 0, 0, 600, 500);

    fill("FF0000");
    stroke("FFA500");

    song_1_status= song_1.isPlaying();
    song_2_status= song_2.isPlaying();

    if(scoreLeftWrist > 0.2){
       circle(leftWristX, leftWristY, 20); 
      song_2.stop();
    if(song_1_status == false){
      song_1.play()
      document.getElementById("song_name").innerHTML="Playing: American Boy - Estelle, Kanye West";
    }
    }

    if(scoreRightWrist > 0.2){
        circle(rightWristX, rightWristY, 20); 
       song_1.stop();
     if(song_2_status == false){
       song_2.play()
       document.getElementById("song_name").innerHTML="Playing: Flashing Lights - Kanye West";
     }
     }
}

function gotPoses(results){
    if(results.length > 0){
        console.log(results);
        scoreLeftWrist = results[0].pose.keypoints[9].score;
        scoreRightWrist = results[0].pose.keypoints[10].score;
        console.log("scoreLeftWrist = " + scoreLeftWrist + "scoreRightWrist = " + scoreRightWrist);

        leftWristX = results[0].pose.leftWrist.x;
        leftWristY = results[0].pose.leftWrist.y;
        console.log("leftWristX = " + leftWristX + "leftWristY = " + leftWristY);
        
        rightWristX = results[0].pose.rightWrist.x;
        rightWristY = results[0].pose.rightWrist.y;
        console.log("rightWristX = " + rightWristX + " rightWristY = " + rightWristY);
    }
}

function modelLoaded(){
    console.log('PoseNet is Initialised.')
}