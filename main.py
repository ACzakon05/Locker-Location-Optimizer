from src.pipeline import pipeline
from src.cities import load_cities, get_bbox, get_expanded_bbox

if __name__ == "__main__":
    cities = load_cities()

    city_name = "Krakow"

    bbox = get_bbox(city_name, cities)
    expanded_bbox = get_expanded_bbox(city_name, cities)

    _, _, recs = pipeline(expanded_bbox, bbox)

    print(recs)