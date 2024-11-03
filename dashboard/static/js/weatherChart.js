$(document).ready( function () {
    getWeather();
    setInterval(updateWeather, 420_000);
});

function get_color(number) {
    if (number <= 50) {
        return "green";
    } else if( number <= 100) {
        return "yellow";
    } else if (number <= 150) {
        return "lightorange";
    } else if (number <= 200) {
        return "orange";
    } else if (number <= 300) {
        return "red";
    } else if (number > 300) {
        return "purple";
    }
}

function createCard(forecast_day) {
    
    return `<div class="card text-light bg-dark mx-4">
        <div class="card-body">
            <p class="card-title ct2">${forecast_day['date']}<br></p>
            
            <div class="col-4"><div class="small-box" background-color="${forecast_day['color']}"></div></div>
            <div class="col-8"><p class="card-text">${forecast_day['Description']}</p></div>
            
        
            <ul class="list-group list-group-flush">
                <li class="list-group-item text-light bg-dark">${forecast_day['precipitation_max']}% ${forecast_day['precipitation_sum']} In.</li>
                <li class="list-group-item text-light bg-dark">${forecast_day['temperature_2m_max']}F - ${forecast_day['temperature_2m_min']}F</li>
            </ul>

        </div>
    </div>`
    
}

function updateWeather() {
    $.ajax({

        // Our sample url to make request 
        url:
            '/weather-data',

        // Type of Request
        type: "GET",

        // Function to call when to
        // request is ok 
        success: function (data) {
            
            $("#temperature").empty();
            $("#temperature").append(`${data["temp"]}F ${data["weather_code"]}`)

            $("#aqi").empty();
            $("#aqi").addClass(get_color(data["aqi"]));
            $("#aqi").append(`AQI: ${data["aqi"]}`);

            $("#forecast").empty();
            for (let i = 0; i < data["forecast"].length; i++) {
                let forecast_day = data["forecast"][i];
                $("#forecast").append(createCard(forecast_day));
            }

            layout = {
                
                paper_bgcolor:'rgba(5,5,5,0.2)',
                plot_bgcolor:'rgba(0,0,0,0)',
                xaxis: {
                    side:'top',
                    titlefont: {
                        family: 'Arial, sans-serif',
                        size: 18,
                        color: 'white'
                      },
                      showticklabels: true,
                      tickangle: 45,
                      tickfont: {
                        family: 'Old Standard TT, serif',
                        size: 14,
                        color: 'white'
                      },
            

                  },

                  yaxis: {
                    showgrid: false,
                    
                    titlefont: {
                        family: 'Arial, sans-serif',
                        size: 18,
                        color: 'white'
                      },
                      showticklabels: true,
                      tickangle: 45,
                      tickfont: {
                        family: 'Old Standard TT, serif',
                        size: 14,
                        color: 'white'
                      },
                
                  }

            }

            Plotly.react('heatmapRain', data["heatmap"],layout);

        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

function getWeather() {
    $.ajax({

        // Our sample url to make request 
        url:
            '/weather-data',

        // Type of Request
        type: "GET",

        // Function to call when to
        // request is ok 
        success: function (data) {
            
            $("#temperature").empty();
            $("#temperature").append(`${data["temp"]}F ${data["weather_code"]}`)

            $("#aqi").empty();
            $("#aqi").addClass(get_color(data["aqi"]));
            $("#aqi").append(`AQI: ${data["aqi"]}`);

            $("#forecast").empty();
            for (let i = 0; i < data["forecast"].length; i++) {
                let forecast_day = data["forecast"][i];
                $("#forecast").append(createCard(forecast_day));
            }
            layout = {
                
                paper_bgcolor:'rgba(5,5,5,0.2)',
                plot_bgcolor:'rgba(0,0,0,0)',
                xaxis: {
                    side:'top',
                    titlefont: {
                        family: 'Arial, sans-serif',
                        size: 18,
                        color: 'white'
                      },
                      showticklabels: true,
                      tickangle: 45,
                      tickfont: {
                        family: 'Old Standard TT, serif',
                        size: 14,
                        color: 'white'
                      },
            

                  },

                  yaxis: {
                    showgrid: false,
                    
                    titlefont: {
                        family: 'Arial, sans-serif',
                        size: 18,
                        color: 'white'
                      },
                      showticklabels: true,
                      tickangle: 45,
                      tickfont: {
                        family: 'Old Standard TT, serif',
                        size: 14,
                        color: 'white'
                      },
                
                  }

            }
            Plotly.newPlot('heatmapRain', data["heatmap"],layout);
        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

