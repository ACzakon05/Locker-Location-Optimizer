import requests
import pandas as pd

def fetch_lockers(bbox):
    url = "https://api-global-points.easypack24.net/v1/points"
    
    # Przekazujemy parametry do API, aby szukało w odpowiednim obszarze
    params = {
        "relative_to": f"{bbox[0]},{bbox[1]}",
        "radius": 50000,
        "per_page": 1000,
        "status": "Operating",
        "type": "parcel_locker",
        "country": "PL"
    }

    try:
        all_items = []
        page = 1
        while True:
            params["page"] = page
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            items = data.get("items", [])
            all_items.extend(items)
            total_pages = data.get("total_pages", 1)
            if page >= total_pages:
                break
            page += 1
        
        # Zawsze zwracamy DataFrame z zadanymi kolumnami, nawet jeśli jest pusty
        cols = ["lat", "lon", "name"]
        if not all_items:
            return pd.DataFrame(columns=cols)

        df = pd.DataFrame(all_items)
        
        # Wyciąganie współrzędnych z zagnieżdżonego słownika location
        df["lat"] = df["location"].apply(lambda x: x["latitude"])
        df["lon"] = df["location"].apply(lambda x: x["longitude"])
        
        # Filtrowanie do dokładnego BBOX
        df = df[
            (df["lat"] >= bbox[0]) & (df["lat"] <= bbox[2]) &
            (df["lon"] >= bbox[1]) & (df["lon"] <= bbox[3])
        ]

        return df[cols] if not df.empty else pd.DataFrame(columns=cols)
        
    except Exception as e:
        print(f"API Connection Error: {e}")
        return pd.DataFrame(columns=["lat", "lon", "name"])