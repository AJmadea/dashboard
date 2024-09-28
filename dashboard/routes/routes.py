from datetime import datetime
from dashboard import app
from flask import render_template, send_file
import requests
from dashboard import nasa, ImagePicker, Weather
from dashboard.njtransit import NJTBusXMLScraper


@app.route('/nasa')
def temp():
    nasa.get_apod()
    return {'3':True}

@app.route("/njt")
def njt():
    return NJTBusXMLScraper.parse_njt().to_html()


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
    return Weather.get_weather_from_file()

@app.route('/')
def home():
    return render_template('test.html')