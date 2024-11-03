from datetime import datetime
import requests, json, os

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from pytz import timezone



weatherCodes=pd.read_csv("dashboard/static/WeatherCodes.csv")

def get_weather_daily_meteo():
    lat=os.getenv("LAT")
    lon=os.getenv("LON")

    #Orlando, FL
    #lat,lon=(28.51339572561113, -81.3767633912537)

    # Chicago-ish
    #lat,lon=(41.850491463149545, -87.90756066948084)

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
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "precipitation_sum"],

        "hourly": ["temperature_2m", "weather_code", "precipitation_probability"],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "forecast_days": 3,
        "timezone": "America/New_York"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

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
    hourly_dataframe= hourly_dataframe[hourly_dataframe.date >= datetime.now()].copy()
    
    hourly_dataframe['Text'] = hourly_dataframe.temperature_2m.astype(str) + "F ("+hourly_dataframe.precipitation_prob.astype(str)+"%) "

    hourly_dataframe.date = pd.to_datetime(hourly_dataframe.date)
    hourly_dataframe.date = hourly_dataframe.date.dt.strftime("%H %P")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_max = daily.Variables(3).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["precipitation_max"] = daily_precipitation_max
    daily_data["precipitation_sum"] = daily_precipitation_sum

    

    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe.precipitation_max = daily_dataframe.precipitation_max.astype(int)
    daily_dataframe.precipitation_sum = daily_dataframe.precipitation_sum.round(2)

    daily_dataframe.precipitation_sum = daily_dataframe.precipitation_sum.astype(str)

    daily_dataframe = daily_dataframe.merge(weatherCodes, how='left')

    return daily_dataframe, current_apparent_temperature, current_precipitation, weatherCodes[weatherCodes.weather_code==current_weather_code].Description.tolist()[0], hourly_dataframe


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
        "minutely_15": ["temperature_2m", "precipitation", "weather_code"],
        "hourly": ["temperature_2m", "weather_code", "precipitation_probability"],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "forecast_days": 2,
        "timezone": "America/New_York"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process minutely_15 data. The order of variables needs to be the same as requested.
    minutely_15 = response.Minutely15()
    minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
    minutely_15_precipitation = minutely_15.Variables(1).ValuesAsNumpy()
    minutely_15_weather_code = minutely_15.Variables(2).ValuesAsNumpy()

    minutely_15_data = {"date": pd.date_range(
        start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
        end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = minutely_15.Interval()),
        inclusive = "left"
    )}
    
    minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
    minutely_15_data["precipitation"] = minutely_15_precipitation
    minutely_15_data["weather_code"] = minutely_15_weather_code

    minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
    print(minutely_15_dataframe)

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