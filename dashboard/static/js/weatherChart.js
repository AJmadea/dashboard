$(document).ready( function () {
    getWeather();
    setInterval(updateWeather(), 420_000);
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

            // weather, aqi
            let _min = 120;
            let _max = -100;
            for (let i = 0; i < data['forecast'][0]['y'].length; i++) {
                if (data['forecast'][0]['y'][i] < _min) {
                    _min = data['forecast'][0]['y'][i];
                } 
                if (data['forecast'][0]['y'][i] > _max) {
                    _max = data['forecast'][0]['y'][i];
                }
            }

            _max *= 1.1;
            _min *= 0.8;

            layout = {
                
                grid: {rows: 1, columns: 2, pattern: 'independent'},
                paper_bgcolor:'rgba(5,5,5,0.2)',
                plot_bgcolor:'rgba(0,0,0,0)',
                xaxis: {
                    showgrid: false,
                    zeroline: true,
                    showline: true,
                    
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
                      exponentformat: 'e',
                      showexponent: 'all'

                  },
                  yaxis2:{
                    showgrid: false,
                    zeroline: true,
                    showline: true,
                    range: [0, 100],
                    
                    gridwidth: 2,
                
                    zerolinewidth: 4,
                    
                    linewidth: 6,
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
                      exponentformat: 'e',
                      showexponent: 'all'
                  },
                  yaxis: {
                    showgrid: false,
                    zeroline: true,
                    showline: true,
                    range: [_min, _max],
                    
                    gridwidth: 2,
                
                    zerolinewidth: 4,
                    
                    linewidth: 6,
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
                      exponentformat: 'e',
                      showexponent: 'all'
                  }
            }


            Plotly.react('weatherChart', data["forecast"], layout);
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

            // weather, aqi
            let _min = 120;
            let _max = -100;
            for (let i = 0; i < data['forecast'][0]['y'].length; i++) {
                if (data['forecast'][0]['y'][i] < _min) {
                    _min = data['forecast'][0]['y'][i];
                } 
                if (data['forecast'][0]['y'][i] > _max) {
                    _max = data['forecast'][0]['y'][i];
                }
            }

            _max *= 1.1;
            _min *= 0.8;

            layout = {
                
                grid: {rows: 1, columns: 2, pattern: 'independent'},
                paper_bgcolor:'rgba(5,5,5,0.2)',
                plot_bgcolor:'rgba(0,0,0,0)',
                xaxis: {
                    showgrid: false,
                    zeroline: true,
                    showline: true,
                    
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
                      exponentformat: 'e',
                      showexponent: 'all'

                  },
                  yaxis2:{
                    showgrid: false,
                    zeroline: true,
                    showline: true,
                    range: [0, 100],
                    
                    gridwidth: 2,
                
                    zerolinewidth: 4,
                    
                    linewidth: 6,
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
                      exponentformat: 'e',
                      showexponent: 'all'
                  },
                  yaxis: {
                    showgrid: false,
                    zeroline: true,
                    showline: true,
                    range: [_min, _max],
                    
                    gridwidth: 2,
                
                    zerolinewidth: 4,
                    
                    linewidth: 6,
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
                      exponentformat: 'e',
                      showexponent: 'all'
                  }
            }


            Plotly.newPlot('weatherChart', data["forecast"], layout);
        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

