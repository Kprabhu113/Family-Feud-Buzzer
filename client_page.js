const big_button = document.querySelector(".big_button");
const quit_button = document.querySelector(".quit_button");
const message = document.getElementById("message");

message.textContent = "Ready to Play";

var hold = false;
var socket = io();
var username = prompt("Enter user name");
socket.emit('join', username);

socket.on("message", (data) => {
    message.textContent = data;
});

socket.on("hold", (data) => {
    if(data == true){
        hold = true;
    }
    else{
        hold = false;
    }
});

big_button.addEventListener("click", ()=> {
    if (hold){
        return;
    }
    socket.emit('button_pressed', "big_button");
});

quit_button.addEventListener("click", ()=>{
    socket.emit('button_pressed', "quit_button");
    socket.disconnect();
});




