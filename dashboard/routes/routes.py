from datetime import datetime
from dashboard import app
from flask import render_template, send_file
import requests
import os
from dashboard import nasa, ImagePicker, Weather, Pexel
from dashboard.njtransit import NJTBusXMLScraper
import pandas as pd

@app.route('/nasa')
def temp():
    hdurl=nasa.get_apod()
    return hdurl

@app.route("/njt")
def njt():
    r= NJTBusXMLScraper.parse_njt().to_dict(orient='records')
    return r

@app.route("/hikes")
def hikes():
    hiking = pd.read_csv("Hikes.csv")
    hiking.time_created = pd.to_datetime(hiking.time_created)
    hiking.distance /= 1610
    totalDistance=round(hiking.distance.sum(),1)
    hiking.distance=hiking.distance.round(2)
    hiking['Hover'] = hiking.title + " " + hiking.distance.astype(str)
    return {"data":hiking.to_dict(orient='list'), 'totalDistance':totalDistance}

@app.route("/bf")
def bf():
    rImage, _file=get_random_image()
    dt=datetime.strptime(_file[:8], "%Y%m%d")
    return render_template('test copy.html', randomImage=rImage, date=dt.strftime("%B -%d %Y"), title=os.getenv("BF_TITLE"))

@app.route('/random-image')
def get_random_image():
    return ImagePicker.get_random_image()

@app.route('/get-temperature')
def temperature():
    from gpiozero import CPUTemperature

    cpu = CPUTemperature()
    return str(round(cpu.temperature * 9/5 + 32,2))

@app.route('/fact-date')
def fact_date():
    now=datetime.now()
    res=requests.get(f"http://numbersapi.com/{now.month}/{now.day}/date")
    res.close()
    return res.text

@app.route("/rt")
def rt():
    pexelPhoto = Pexel.get_seasonal_image()
    nasa=temp()
    rImage, _file=get_random_image()

    dt=datetime.strptime(_file[:8], "%Y%m%d")
    dt = dt.strftime("%B %d, %Y")

    return render_template('revealTest.html', randomImage=rImage, date=dt, alt=pexelPhoto['alt'],
        url=pexelPhoto['src']['large2x'], title="Maywood Boys", hdurl=nasa["hdurl"], nasaTitle=nasa["title"], nasaDescription=nasa["explanation"])

@app.route("/weather-data")
def get_weather():
    # hourly_dataframe, current_apparent_temperature, current_precipitation, current_weather_code
    
    data = Weather.get_weather_daily_meteo()
    daily_data=data[0]
    hourly_data = data[-1]
    hourly_data = hourly_data[['date','precipitation_prob']].copy()

    hourly_data.date = pd.to_datetime(hourly_data.date)
    hourly_data['Hour'] = hourly_data.date.dt.time
    #hourly_data.Hour = hourly_data.date.dt.strftime("%I%p")
    hourly_data.sort_values(by='date', inplace=True, ascending=True)
    hourly_data['date'] = hourly_data.date.dt.date

    
    #hourly_data.Hour = hourly_data.Hour.astype(str)
    hourly_data.date = hourly_data.date.astype(str)

    hourly_data = hourly_data.pivot(index='date',columns='Hour', values='precipitation_prob')
    hourly_data = hourly_data.fillna(0)

    hourly_data.columns = [x.strftime("%I%p") for x in hourly_data.columns.tolist()]
    
    opacities = [
        [0, 'rgba(0, 80, 0, 0.0)'], 
        [0.10, 'rgba(0, 80, 0, 0.0)'], 

        [0.10, 'rgba(0, 80, 0, 0.1)'], 
        [0.20, 'rgba(0, 80, 0, 0.2)'], 

        [0.20, 'rgba(0, 80, 0, 0.2)'], 
        [0.30, 'rgba(0, 80, 0, 0.3)'], 

        [0.30, 'rgba(0, 80, 0, 0.3)'], 
        [0.40, 'rgba(0, 80, 0, 0.4)'], 

        [0.40, 'rgba(0, 80, 0, 0.4)'], 
        [0.50, 'rgba(0, 80, 0, 0.5)'], 

        [0.50, 'rgba(0, 80, 0, 0.5)'], 
        [0.60, 'rgba(0, 80, 0, 0.6)'], 

        [0.60, 'rgba(0, 80, 0, 0.6)'], 
        [0.70, 'rgba(0, 80, 0, 0.7)'], 

        [0.70, 'rgba(0, 80, 0, 0.7)'], 
        [0.80, 'rgba(0, 80, 0, 0.8)'], 

        [0.80, 'rgba(0, 80, 0, 0.8)'], 
        [0.90, 'rgba(0, 80, 0, 0.9)'], 

        [0.90, 'rgba(0, 80, 0, 0.9)'], 
        [1.00, 'rgba(0, 80, 0, 1.0)']
    ]



    heatmap=[{
        'x':hourly_data.columns.tolist(),
        'y':hourly_data.index.tolist(),
        'z':hourly_data.values.tolist(),
        'type':'heatmap',
        'colorscale': opacities,
        'zmin': 0,
        'zmax': 100,
        'showscale':False
    }]



    daily_data.temperature_2m_max = daily_data.temperature_2m_max.astype(int)
    daily_data.temperature_2m_min = daily_data.temperature_2m_min.astype(int)
    daily_data.date = daily_data.date.dt.strftime("%a %b %d")
    
    dict_data= {'forecast':daily_data.to_dict(orient='records'), 'temp':int(data[1]), 'precipitation':round(data[2],2), 'weather_code':data[3], 'aqi': int(Weather.get_aqi()), 
                'heatmap':heatmap}
    
    return dict_data


@app.route('/')
def home():
    pexelPhoto = Pexel.get_seasonal_image()

    title=os.getenv("TITLE")

    return render_template('test.html', backgroundImage=pexelPhoto['src']['large2x'], title=title, averageColor=pexelPhoto['avg_color'])