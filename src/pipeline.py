import pandas as pd
from src.etl import fetch_lockers
from src.grid import generate_grid
from src.population import PopulationData
from src.geo import haversine_distances, count_neighbors_within
from src.scoring import compute_scores, filter_candidates
from src.clustering import cluster_points
from src.config import *

def pipeline(bbox):
    lockers_df=fetch_lockers(bbox)
    if lockers_df.empty:
        return None,None,None
    grid_df= generate_grid(bbox,spacing_m=GRID_SPACING_METERS)

    pop=PopulationData("data/population.tif")

    grid_df["population"]=grid_df.apply(
        lambda row: pop.get_population(row["lat"], row["lon"]),
        axis=1
    )

    distances, _=haversine_distances(
        grid_df[["lat", "lon"]].values,
        lockers_df[["lat", "lon"]].values
    )

    grid_df["distance"]=distances

    grid_df["locker_density"]=count_neighbors_within(
        grid_df[["lat","lon"]],
        lockers_df[["lat", "lon"]],
        1000                      
    )

    grid_df=compute_scores(grid_df)
    filtered=filter_candidates(grid_df)

    clustered=cluster_points(filtered)

    clustered["explanation"] = clustered.apply(
        lambda row: f"High population ({row['population']:.1f}) and far from lockers ({row['distance']:.0f}m)",
        axis=1
    )

    return grid_df, lockers_df, clustered.head(TOP_N)