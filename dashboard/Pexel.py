import PIL.Image
import requests,json
import os
from datetime import datetime, date
import pandas as pd

import PIL

specificDates = pd.read_excel('dashboard/static/specificDates.xlsx')
specificDates.set_index(['Month','Day'], inplace=True)

season_map = pd.read_excel('dashboard/static/monthQueries.xlsx')
season_map.set_index('Month', inplace=True)


def get_seasonal_image():
    PEXEL_API_KEY = os.getenv('PEXEL_API_KEY')

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Authorization": PEXEL_API_KEY
    }

    dt=datetime.now().date()

    try:
        query = specificDates.loc[(dt.month, dt.day), 'Query']
    except:
        query = None


    try:
        season = season_map.loc[dt.month, 'Query']
    except: 
        season= None


    query = query or season
    #{dt.strftime('%B')}
    print(query)
    res=requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=32&orientation=landscape&size=large", headers=headers)
    res.close()
    
    return res.json()['photos'][dt.day]

def get_image():

    PEXEL_API_KEY = os.getenv('PEXEL_API_KEY')

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Authorization": PEXEL_API_KEY
    }

    dt=datetime.now().date()

    res=requests.get(f"https://api.pexels.com/v1/search?query=october scenery {dt.strftime('%B')}&per_page=32&orientation=landscape", headers=headers)
    res.close()
    
    url = res.json()['photos'][dt.day]
    return url