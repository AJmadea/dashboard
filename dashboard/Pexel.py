import requests,json
import os
from datetime import datetime



def get_seasonal_image():

    PEXEL_API_KEY = os.getenv('PEXEL_API_KEY')

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Authorization": PEXEL_API_KEY

    }

    dt=datetime.now().date()

    res=requests.get(f"https://api.pexels.com/v1/search?query=october scenery {dt.strftime('%B')}&per_page=32&orientation=landscape&size=large", headers=headers)
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
    
    return res.json()['photos'][dt.day]