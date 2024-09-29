$(document).ready( function () {
    updateTime();

    setInterval(updateTime,1000);
});


function updateTime() {
    
    let dt= new Date();
    $("#datetime").empty();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    };

    $("#datetime").append(dt.toLocaleDateString("en-US", options));
}

