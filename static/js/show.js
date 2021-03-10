import {apiHandler} from "./api-handler.js";


const popupActor = document.getElementById("popup-actor");
const actorsButtons = document.getElementById("actors");
const popupGenres = document.getElementById("popup-genres");
const bodyWrapper = document.getElementById("body-wrapper");

function init(){
    addListener();
}

function addListener(){
    actorsButtons.addEventListener('click', onClickHandlers);
    popupActor.addEventListener('click', onClickHandlers)
}

function onClickHandlers(evt){
    if (evt.target.classList.contains("actor-details")){
        let actor_id = evt.target.value;
        getActorDetails(actor_id);
    }
    if (evt.target.id === "show-genres") {
        let actor_id = evt.target.value;
        apiHandler.api_get(`/actors/genres/${actor_id}`, function (response) {
            let content = response['gatunki']
            popupGenres.innerHTML = `<div>${content}</div>`

            popupGenres.style.display = "block";

        })
    }

}


function getActorDetails(actor_id) {
    apiHandler.api_get(`/actor/${actor_id}`, function (response){
        if (response['status']=== "wrong_id" ){
            console.log("Incorrect id")
        }
        else {
            let content = `
                            <div class="close-line"><i class="close" >&#x292B;</i></div>
                          <div>Name: ${response.name}</div>
                          <div>Birthday: ${response.birthday}</div>
                          <div>Death: ${response.death}</div>
                          <div>Biography: ${response.biography}</div>
                          <button id="show-genres" value="${actor_id}">Genres</button> `


            popupActor.innerHTML = content;
            popupActor.style.display = "block";

        }
    })
}


init();



function addDirector() {

    apiHandler.api_get('https://api.trakt.tv/shows/'+currentShowId+'/people', function (response) {
        let directorDiv= document.getElementById("director");
        let responss = response;
        let directors = response['crew']['directing'];

        let directorsString="";
        for (let director of directors){
            directorsString += director['person']['name']+","
        }

        directorDiv.innerText = directorsString.slice(0,-1);
    })

};
