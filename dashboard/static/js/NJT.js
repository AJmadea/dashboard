$(document).ready( function () {
    updateNJT();
});

function create_card(bus, description,title) {
    return `<div class="card text-light bg-dark pt-5">
        <div class="card-body">
            <h5 class="card-title">${bus}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${title}</h6>
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

            if (data.length == 0) {
                $("#NJT").hide();

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

