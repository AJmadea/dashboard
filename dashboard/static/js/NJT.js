$(document).ready( function () {
    updateNJT();
    setInterval(updateNJT, 60_000)
});

function create_card(bus, description,title) {
    return `<div class="card text-light bg-dark m-1">
        <div class="card-body">
            <p class="card-title">Bus #${bus}</p>
            <p class="card-subtitle mb-2 text-muted">${title}</p>
            <p class="card-text">${description}</p>
            
        </div>
    </div>`
}

function updateNJT() {
    $.ajax({

        // Our sample url to make request 
        url:
            '/njt',

        // Type of Request
        type: "GET",

        // Function to call when to
        // request is ok 
        success: function (data) {
            
            $("#NJT").empty();
            //$("#NJT").append("NJ Transit Advisories");

            if (data.length == 0) {
                //$("#NJT").hide();
                $("#NJT").append("<br>No Advisories!");
                /*$("#weatherCol").addClass("col");
                $("#weatherCol").removeClass("col-8");*/
            } else { 
                $("#NJT").show();
                /*$("#weatherCol").removeClass("col");
                $("#weatherCol").addClass("col-8");*/
            }

            for (let i=0; i<data.length;i++) {
                let card= create_card(data[i]["Bus"], data[i]["Description"],data[i]["Title"]);
               
                $("#NJT").append(card);
            }
            

        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

