let date = new Date();

$(document).ready( function () {
    updateTemp();

    setInterval(updateTemp, 20000);
});

function updateTemp() {
    let current= new Date();
    if ((date.getTime() - current.getTime() >= 8) || date.getDay()!=current.getDay()) {
        location.reload();
    }

    $.ajax({

        // Our sample url to make request 
        url:
            '/get-temperature',

        // Type of Request
        type: "GET",

        // Function to call when to
        // request is ok 
        success: function (data) {
            
            $("#pi").empty();
            $("#pi").append(data);
            

        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

