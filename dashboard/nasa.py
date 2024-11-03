import requests
import json
import os

def get_apod():
    NASA_API_KEY= os.getenv("NASA_API_KEY")

    res=requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}")
    res.close()
    jData=res.json()

    #hdUrl=jData.get('hdurl','')
    return jData