import rasterio 
import numpy as np

class PopulationData:
    def __init__(self, raster_path):
        self.dataset=resterio.open(raster_path)

    def get_population(self, lat, lon):
        try:
            row,col=self.dataset.index(lon,lat)
            value=self.dataset.read(1)[row,col]

            if np.isnan(value):
                return 0

            return float(value)
        except:
            return 0