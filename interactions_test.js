
function check_click(big_button, quit_button){
    big_button.onclick = () => {
        message.textContent = "Big button clicked"
    };
    quit_button.onclick = () =>{
        message.textContent = "Quit button clicked"
    };
};

window.addEventListener("DOMContentLoaded", () => {
    const big_button = document.querySelector(".big_button");
    const quit_button = document.querySelector(".quit_button");
    const message = document.getElementById("message");

    check_click(big_button, quit_button, message);
});




