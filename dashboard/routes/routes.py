from datetime import datetime
from dashboard import app
from flask import render_template, send_file
import requests
import os
from dashboard import nasa, ImagePicker, Weather, Pexel
from dashboard.njtransit import NJTBusXMLScraper


@app.route('/nasa')
def temp():
    nasa.get_apod()
    return {'3':True}

@app.route("/njt")
def njt():
    
    r= NJTBusXMLScraper.parse_njt().to_dict(orient='records')
    
    return r


@app.route('/random-image')
def get_random_image():
    return send_file(ImagePicker.get_random_image(), mimetype='image/jpg')

@app.route('/fact-date')
def fact_date():
    now=datetime.now()
    res=requests.get(f"http://numbersapi.com/{now.month}/{now.day}/date")
    res.close()
    return res.text

@app.route("/weather-data")
def get_weather():
    # hourly_dataframe, current_apparent_temperature, current_precipitation, current_weather_code
    
    data = Weather.get_weather_meteo()
    

    trace1 = {
        'x': data[0]['date'].tolist(),
        'y': data[0]['temperature_2m'].tolist(),
        'text': data[0]['temperature_2m'].tolist(),
        'marker':{
            'color': data[0]['color'].tolist(),
            
            'textposition': 'auto',

        },
        'type': 'bar'
    }

    trace2 ={
        'x': data[0]['date'].tolist(),
        'y': data[0]['precipitation_prob'].tolist(),
        'text': data[0]['precipitation_prob'].tolist(),
        'type':'line',
        'xaxis': 'x2',
        'yaxis': 'y2',
        'title':"Rain % Chance"
    }

    print(data[0].Description.tolist())
    dict_data= {'forecast':[trace1,trace2], 'temp':int(data[1]), 'precipitation':round(data[2],2), 'weather_code':data[3], 'aqi': int(Weather.get_aqi())}
    
    return dict_data


@app.route('/')
def home():
    pexelPhoto = Pexel.get_seasonal_image()

    title=os.getenv("TITLE")

    return render_template('test.html', backgroundImage=pexelPhoto['src']['large2x'], title=title, averageColor=pexelPhoto['avg_color'])