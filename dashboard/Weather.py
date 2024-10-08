from datetime import datetime
import requests, json, os

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from pytz import timezone

def get_weather_from_api():
    w_api = os.getenv("WEATHER_API_KEY")
    res=requests.get(f"http://api.weatherstack.com/current?access_key={w_api}&query=Maywood New Jersey&units=f")
    return res.json()

def get_weather_from_file():
    with open("weatherDataSample.json",'r') as f:
        weatherData=json.load(f)
    return weatherData

weatherCodes=pd.read_csv("dashboard/static/WeatherCodes.csv")

def get_weather_meteo():
    lat=os.getenv("LAT")
    lon=os.getenv("LON")

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 60)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "precipitation", "weather_code"],
        "hourly": ["temperature_2m", "weather_code", "precipitation_probability"],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "forecast_days": 2,
        "timezone": "America/New_York"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_apparent_temperature = current.Variables(0).Value()
    current_precipitation = current.Variables(1).Value()
    current_weather_code = current.Variables(2).Value()

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
    hourly_prob = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc=True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc=True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data['precipitation_prob']=hourly_prob

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe.date = hourly_dataframe.date.dt.tz_convert("America/New_York")
    hourly_dataframe.precipitation_prob = hourly_dataframe.precipitation_prob.astype(float)
    
    hourly_dataframe.precipitation_prob=hourly_dataframe.precipitation_prob.round(2)

    hourly_dataframe= hourly_dataframe.merge(weatherCodes)

    hourly_dataframe.temperature_2m = hourly_dataframe.temperature_2m.round(0)
    hourly_dataframe.precipitation_prob = hourly_dataframe.precipitation_prob.round(2)

    hourly_dataframe.date = hourly_dataframe.date.dt.tz_convert(None)
    hourly_dataframe= hourly_dataframe[hourly_dataframe.date > datetime.now()].copy()
    
    hourly_dataframe['Text'] = hourly_dataframe.temperature_2m.astype(str) + "F ("+hourly_dataframe.precipitation_prob.astype(str)+"%) "

    hourly_dataframe.date = pd.to_datetime(hourly_dataframe.date)
    hourly_dataframe.date = hourly_dataframe.date.dt.strftime("%H %P")
    
    return hourly_dataframe, current_apparent_temperature, current_precipitation, weatherCodes[weatherCodes.weather_code==current_weather_code].Description.tolist()[0]

def get_aqi():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    lat=os.getenv("LAT")
    lon=os.getenv("LON")
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_us_aqi = current.Variables(0).Value()

    
    return current_us_aqi