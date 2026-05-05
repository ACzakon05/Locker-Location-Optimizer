import numpy as np
import pandas as pd

def generate_grid(bbox, spacing_m=400):
    min_lat, min_lon, max_lat, max_lon=bbox

    lat_step=spacing_m/111320   #zamiana ze stopni na metry
    lon_step=spacing_m/(111320 * np.cos(np.radians(min_lat))) 

    lats=np.arange(min_lat, max_lat, lat_step)
    lons=np.arange(min_lon, max_lon,lon_step)

    grid=[(lat,lon) for lat in lats for lon in lons]

    return pd.DataFrame(grid, columns=["lat", "lon"])