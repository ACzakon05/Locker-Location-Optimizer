import numpy as np
from src.config import *
from sklearn.preprocessing import MinMaxScaler

def compute_scores(df):
    if df.empty:
        return df
    
    scaler=MinMaxScaler()
    cols_to_scale = ["population", "distance", "raw_gap"]
    df["raw_gap"]=1/ (1+ df["locker_density"])
    df[[f"{c}_norm" for c in cols_to_scale]] = scaler.fit_transform(df[cols_to_scale])
    df["score"] = (
        0.7 * df["population_norm"] + 
        0.2 * df["distance_norm"] + 
        0.1 * df["raw_gap_norm"]
    )
    return df

def filter_candidates(df):
    df=df[
        (df["distance"]> DISTANCE_THRESHOLD_METERS) &
        (df["population"]>POPULATION_THRESHOLD)
    ]

    threshold=df["score"].quantile(TOP_PERCENTILE)
    return df[df["score"]>=threshold]