$(document).ready( function () {
    updateFact();
});

function updateFact() {
    $.ajax({

        // Our sample url to make request 
        url:
            '/fact-date',

        // Type of Request
        type: "GET",

        // Function to call when to
        // request is ok 
        success: function (data) {
            
            $("#factoid").empty();
            $("#factoid").append(data);
            

        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

