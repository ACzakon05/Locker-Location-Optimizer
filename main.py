from src.pipeline import run_pipeline
from src.cities import load_cities, get_bbox

if __name__ == "__main__":
    cities = load_cities()
    bbox = get_bbox("Krakow", cities)

    _, _, recs = run_pipeline(bbox)

    print(recs)