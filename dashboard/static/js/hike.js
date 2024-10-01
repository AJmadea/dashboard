$(document).ready( function () {
    createMap();

});



function createMap() {
    $.ajax({

        // Our sample url to make request 
        url:
            '/hikes',

        // Type of Request
        type: "GET",

        // Function to call when to
        // request is ok 
        success: function (data) {
            let total = data["totalDistance"];
            data = data["data"];

            $("#totalHiking").append(`${total} Miles Walked Together`);

            var plotlyData = [{
                type: 'scattergeo',
                mode: 'markers+text',
                
                lon: data["longitude"],
                lat: data["latitude"],
                hovertext: data['Hover'],
                marker: {
                    color: data['hexcolor']
                },
                name: 'Canadian cities',
            }];
            
            var layout = {
                paper_bgcolor:'rgba(5,5,5,0.2)',
                plot_bgcolor:'rgba(0,0,0,0)',
                title: 'Hiking Data',
                font: {
                    family: 'Droid Serif, serif',
                    size: 6
                },
                titlefont: {
                    size: 16
                },
                geo: {
                    scope: 'north america',
                    resolution: 50,
                    lonaxis: {
                        'range': [-80.6667, -72.9448]
                    },
                    lataxis: {
                        'range': [39.0179,43.6667]
                    },
                    showrivers: true,
                    rivercolor: '#fff',
                    showlakes: true,
                    lakecolor: '#fff',
                    showland: true,
                    landcolor: '#EAEAAE',
                    countrycolor: '#d3d3d3',
                    countrywidth: 1.5,
                    subunitcolor: '#d3d3d3'
                }
            };
            
            Plotly.newPlot('hikingMap', plotlyData, layout);

        },

        // Error handling 
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}
