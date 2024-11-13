let date = new Date();

$(document).ready( function () {
    updateTime();

    setInterval(updateTime,1000);
});

function weatherWidget() {
    let widget = `<a class="weatherwidget-io" href="https://forecast7.com/en/40d90n74d06/maywood/?unit=us" data-label_1="Maywood" data-label_2="Weather" data-font="Times New Roman" data-icons="Climacons Animated" data-theme="original" >Maywood Weather</a>
    
    `;

    $("#weatherwidget").empty();
    $("#weatherwidget").append(widget);
}

function updateTime() {

    let current= new Date();
    if ((date.getTime() - current.getTime() >= 3) || date.getDay()!=current.getDay()) {
        location.reload();
    }

    //weatherWidget();

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

