import json

def load_cities(path="data/cities.json"):

    with open(path) as f:
        return json.load(f)
    
def get_bbox(city_name, cities):
    for city in cities:
        if city["name"]==city_name:
            return city["bbox"]
        
    raise ValueError("City not found")

def get_expanded_bbox(city_name, cities, buffer=0.03):
    bbox = get_bbox(city_name, cities)
    return [bbox[0] - buffer, bbox[1] - buffer, bbox[2] + buffer, bbox[3] + buffer]
