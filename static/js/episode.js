import {apiHandler} from "./api-handler.js";

const showList = document.getElementById("form-example-show");
const formContainer = document.querySelector("form");
const seasonList = document.getElementById("form-example-season");
const episodeList = document.getElementById("form-example-episode");
const episodeTitleInput = document.getElementById("form-example-title");
const episodeLength = document.getElementById("form-example-length");


function init() {
    prepareShowList();
    addEpisodeEventListener();
}

function prepareShowList() {

    apiHandler.api_get('/get-shows', function (response){
        let shows = ""
        for (let show of response) {
            shows += `
                <option value="${show.id}">${show.title}</option>`
        }

        showList.innerHTML = shows
    })


}

function addEpisodeEventListener() {
    formContainer.addEventListener('change', onSelectHandler)

}

function onSelectHandler(evt) {
    if (evt.target.id === "form-example-show") {
        let show_id = evt.target.value;

        let seasons = "";
        apiHandler.api_get(`/get-seasons/${show_id}`, function (response) {
            for (let season of response){
                seasons += `
                            <option value=${season.id}>${season.title}</option>`
            }
        seasonList.innerHTML = seasons;

        })
    }

    if (evt.target.id === "form-example-season"){
        let season_id = evt.target.value;

        let episodes = "";
        apiHandler.api_get(`/get-episodes/${season_id}`, function (response){
            for (let episode of response){
                episodes += `
                        <option value=${episode.id}>${episode.title}</option>`
            }
        episodeList.innerHTML = episodes;
        })
    }

    if (evt.target.id === "form-example-episode"){
        let episodeTitle = evt.target.options[evt.target.selectedIndex].text;


        episodeTitleInput.placeholder = episodeTitle;
        episodeTitleInput.setAttribute("data-episode-id",evt.target.value);

        apiHandler.api_get(`/get-episode-length/${evt.target.value}`, function (response) {
            let a = response;
            episodeLength.value = response['episode_number'];

        })


    }
}


init()