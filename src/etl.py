#extract, transform, load

import requests
import pandas as pd

API_URL = "https://api-global-points.easypack24.net/v1/points"

def fetch_lockers(bbox):
    params={
        "type": "parcel_locker",
        "per_page": 500,
        "page": 1
    }

    all_points=[]

    while True:
        response=requests.get(API_URL, params=params)
        data=response.json()
        if "items" not in data:
            break
        
        for item in data["items"]:
            lat=item["location"]["latitude"]
            lon=item["location"]["longitude"]

            if bbox[0]<=lat <= bbox[2] and bbox[1]<=bbox[3]:
                all_points.append((lat,lon))

        if not data.get("meta", {}).get("has_next_page"):
            break
        params["page"]+=1
    return pd.DataFrame(all_points, colums=["lat","lon"])