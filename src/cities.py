import json

def load_cities(path="data/cites.json"):

    with open(path) as f:
        return json.load(f)
    
def get_bbox(city_name, cities):
    for city in cities:
        if city["name"]==city_name:
            return city["bbox"]
        
    raise ValueError("City not found")

    
