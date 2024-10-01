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
    nasa.get_apod()
    return {'3':True}

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
    hourly_dataframe=data[0]
    #data[0]['precipitation_prob'] = range(data[0]['precipitation_prob'].shape[0])
    #data[0]['precipitation_prob'] = 100
    trace1 = {
        'x': data[0]['date'].tolist(),
        'y': data[0]['temperature_2m'].tolist(),
        'text': data[0]['Text'].tolist(),
        'marker':{
            'color': data[0]['precipitation_prob'].tolist(),
            'textposition': 'auto',
            'colorscale': 'Portland',
            'size':15
        },
        
        'mode': 'lines+markers'
    }

    hourly_dataframe['change'] = hourly_dataframe.weather_code.diff()
    hourly_dataframe.change = hourly_dataframe.change.fillna(0)
    
    changes=pd.concat([hourly_dataframe.head(1),hourly_dataframe[hourly_dataframe.change!=0]]).reset_index()
    changeList=[]

    for i in changes.index[:-1]:
        changeList.append({"x0":changes.loc[i,'date'],'x1':changes.loc[i+1,'date'],'fillcolor':changes.loc[i,'color'], 'opacity':0.2,'y0':-20, 'y1':120,
                           'label': {'text': changes.loc[i, 'Description'], 'font': { 'size': 8, 'color': 'white' }}})

    
    dict_data= {'forecast':[trace1], 'temp':int(data[1]), 'precipitation':round(data[2],2), 'weather_code':data[3], 'aqi': int(Weather.get_aqi()), 'changes':changeList}
    
    return dict_data


@app.route('/')
def home():
    pexelPhoto = Pexel.get_seasonal_image()

    title=os.getenv("TITLE")

    return render_template('test.html', backgroundImage=pexelPhoto['src']['large2x'], title=title, averageColor=pexelPhoto['avg_color'])