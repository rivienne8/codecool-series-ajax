import {apiHandler} from "./api-handler.js";


const registerButton = document.getElementById("bt-register");
const loginButton = document.getElementById("bt-login");
const bodyWrapper = document.getElementById("body-wrapper");
const popupBox = document.getElementById("popup");


function init() {
    addListeners();

}

function addListeners() {
    registerButton.addEventListener('click', onClickHandler );
    loginButton.addEventListener('click', onClickHandler);
    popupBox.addEventListener('click', onClickHandler);

}

function onClickHandler(evt) {
    if (evt.target.id === "bt-register") {
        let insertion = prepareRegisterLoginPopup();
        showPopup(insertion);
    }

    if (evt.target.classList.contains("close")){
        evt.target.closest(".popup").style.display = "none";
        bodyWrapper.style.removeProperty("opacity");
        evt.target.closest(".popup").innerHTML ="";
    }

    if (evt.target.id === "bt-login") {
        let insertion = prepareRegisterLoginPopup(true);
        showPopup(insertion);
    }


}

function prepareRegisterLoginPopup(login) {
    let message = "SUBMIT";
    let target = "/register";
    if(login){
        message = "LOGIN";
        target = "/login";
    }

    let insertion = `   
            <p class="form-element">
                <p class="close-line"><i class="close" >&#x292B;</i></p>
                <form action=${target} method="POST">
                    <label for="username" class="form-element-label">Username:</label>
                    <input name="username" id="username" type="text" required minlength="3">
                    <label for="password" class="form-element-label">Password:</label>
                    <input name="password" id="password" type="password" required minlength="3">
                    <p class="close-line" ><button type="submit">${message}</button></p>
                </form>      
            </p>`

    return insertion;

}

function showPopup(insertion){
    popupBox.style.display = "block";
    bodyWrapper.style.opacity = "0.2";
    popupBox.insertAdjacentHTML("beforeend", insertion);
}

init();