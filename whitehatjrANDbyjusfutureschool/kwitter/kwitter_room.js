import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyB3SDYJD220qMq5q1nVOeCd3qNCMa35RdY",
  authDomain: "messagestore-eeaa3.firebaseapp.com",
  databaseURL: "https://messagestore-eeaa3-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "messagestore-eeaa3",
  storageBucket: "messagestore-eeaa3.appspot.com",
  messagingSenderId: "792713290078",
  appId: "1:792713290078:web:91d8ff1ecbbd2042136fcf"
};  

const app = initializeApp(firebaseConfig);

    function addUser()
{
  user_name = document.getElementById("user_name").value;
  firebase.database().ref("/").child(user_name).update({
    purpose : "adding user"
  });
}

function getData() {firebase.database().ref("/").on('value', function(snapshot) {document.getElementById("output").innerHTML = "";snapshot.forEach(function(childSnapshot) {childKey  = childSnapshot.key;
       Room_names = childKey;
      console.log("Room Name - " + Room_names);
      row = "<div class='room_name' id="+Room_names+"onclick='redirectToRoomName(this.id)' >#"+Room_names+"</div><hr>";
      document.getElementById("output").innerHTML += row;
      });});}
getData();

function onClick()

function redirectToRoomName(name){
  console.log(name);
  localStorage.setItem("room_name", name);
  window.location = "kwitter_page.html";
}

function logout(){
  localStorage.removeItem("user_name");
  localStorage.removeItem("room_name");
  window.location = "kwitter.html";
}

function send(){
  msg = document.getElementById("msg").value;
  firebase.database().ref(room_name).push({
    name: user_name,
    message:msg,
    like:0
  });
  document.getElementById("msg").value = "";
}