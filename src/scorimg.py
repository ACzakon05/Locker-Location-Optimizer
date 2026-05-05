import numpy as np
from src.config import *

def compute_scores(df):
    df["gap_factor"]=1/ (1+ df["locker_density"])
    df["score"]=df["population"] * df["distance"] * df["gap_factor"]
    return df

def filter_candidates(df):
    df=df[
        (df["distance"]> DISTANCE_THRESHOLD_METERS) &
        (df["population"]>POPULATION_THRESHOLD)
    ]

    threshold=df["score"].quantile(TOP_PERCENTILE)
    return df[df["score"]>=threshold]