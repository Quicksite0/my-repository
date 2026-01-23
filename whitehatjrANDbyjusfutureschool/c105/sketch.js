camera = document.getElementById("camera");
      
Webcam.attach( camera );      
  Webcam.set({
    width:350,
    height:300,
    image_format : 'png',
    png_quality:90
  });


function gotResult(error, results) {
  if (error) {
    console.error(error);
  } else {
    console.log(results);
    
    /*write code to 
    1.Store the speech API in variable synth, 
    2.Store the data in variable speak_data that we want the system to speak ,
    3.Use the SpeechSynthesisUtterance() function to convert the text to speech that we have saved in variable speak_data.
    4.then use synth.speak() to read out the text provided
    5.Update the object name and accuracy as we have done before.
    
    
    */
  }
}

function take_snapshot()
{
    Webcam.snap(function(data_uri) {
        document.getElementById("result").innerHTML = '<img id="selfie_image" src="'+data_uri+'"/>';
    });
}

  console.log('ml5 version:', ml5.version);
  
classifier = ml5.imageClassifier('https://teachablemachine.withgoogle.com/models/v_sl95BzE/model.json',modelLoaded);

  function modelLoaded() {
    console.log('Model Loaded!');
  }
      
  function check()
  {
    //write code to store the selfie_image in a variable img and then use classify() function to classify it
  
  }
