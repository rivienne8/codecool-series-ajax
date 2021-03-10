
export let apiHandler = {

    api_get: function (url, callback){
        fetch(url)
            .then((response) => response.json())
            .then((data) => callback(data))
            .catch(rejected => {
                callback(null)
            })
    },

    api_post: function (url, data, callback) {
        fetch(url, {
            method: "POST",
            credentials: "same-origin",
            headers: {"Content-Type" : "application/json"},
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => callback(data))
            .catch(rejected => {
                console.log(rejected)
                callback(null)
            });
    }
}