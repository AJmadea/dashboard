import pandas as pd
import requests
from xml.etree import ElementTree
import os
from datetime import datetime, timedelta

def parse_njt():
    res=requests.get("http://njtransit.com/rss/BusAdvisories_feed.xml")
    res.close()

    tree = ElementTree.fromstring(res.text)

    root=tree[0][7:]

    titles=[]
    desc=[]
    nodes=[]
    dates=[]

    for advisory in root:
        if advisory.tag=='item':
            titles.append(advisory.find('title').text)
            desc.append(advisory.find('description').text)
            nodes.append(advisory.find("link").text.split("/")[-1])
            dates.append(advisory.find("pubDate").text)
        
    df = pd.DataFrame({"Title":titles,'Description':desc,'Node':nodes,'DateTime':dates})
    df['Bus'] = df.Title.apply(lambda x: x.split("-")[0])
    df.Bus = df.Bus.str.replace("BUS ",'',regex=False)
    df.Bus = df.Bus.str.strip()
    df.Bus = df.Bus.astype(int)
    df.sort_values(by='Bus', inplace=True)
    
    df.DateTime = pd.to_datetime(df.DateTime)
    df= df[df.DateTime >= (datetime.now() - timedelta(days=7))]
    df.sort_values(by="DateTime", ascending=False, inplace=True)
    
    old_adv = pd.read_csv('Advisories.csv')

    old_adv = old_adv.merge(df, on='Title', how='right', indicator=True)
    old_adv=old_adv[old_adv._merge=='right_only'].copy()
    print(old_adv)

    new_advisories = df[df.Title.isin(old_adv.Title.unique())].copy()


    new_advisories.to_csv('Advisories.csv', index=False, mode='a', header=False)

    df=df[df.Bus.isin({772,168,751,755,752})].copy()

    return df