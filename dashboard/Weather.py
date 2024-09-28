import requests, json, os

def get_weather_from_api():
    w_api = os.getenv("WEATHER_API_KEY")
    res=requests.get(f"http://api.weatherstack.com/current?access_key={w_api}&query=Maywood New Jersey&units=f")
    return res.json()

def get_weather_from_file():
    with open("weatherDataSample.json",'r') as f:
        weatherData=json.load(f)
    return weatherData