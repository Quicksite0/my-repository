song = "";
Status = "";
objects = [];

function preload(){
    song = loadSong("Alarm.html");
}
function setup() {
    canvas = createCanvas(380, 380);
    canvas.center();
    video = createCapture(VIDEO);
    video.size(380,380);
    video.hide();

    objectDetector = ml5.objectDetector('cocossd', modelLoaded);
    document.getElementById("status").innerHTML = "Status : Detecting Objects";
    
}


function draw() {
    image(video, 0, 0, 380, 380);
    
    if (Status != "") {
        objectDetector.detect(video, gotResult);
        for (i = 0; i < objects.length; i++) {
            document.getElementById("status").innerHTML = "Status : Object Detected";
            fill("#0000FF");
            percent = floor(objects[i].confidence * 100);
            text(objects[i].label + " " + percent + "%", objects[i].x + 15, objects[i].y + 15);
            noFill();
            stroke("#0000FF");
            rect(objects[i].x, objects[i].y, objects[i].width, objects[i].height);

            if(objects[i].label == "person")
            {
                document.getElementById("noo").innerHTML = "Baby Found";
                console.log("stop");
                song.stop();
            }
            else{
                document.getElementById("noo").innerHTML = "Baby Not Found";
                console.log("play");
                song.play();
            }
        }
    }
    

}

function modelLoaded() {
    console.log("Model is Loaded");
    Status = true;
    

}

function gotResult(error, results) {
    if (error) {
        console.log(error);
    }
    console.log(results);
    objects = results;

}
 