import numpy as np
from sklearn.cluster import DBSCAN
from src.config import DBSCAN_EPS_METERS

def cluster_points(df):
    coords=np.radians(df[["lat", "lon"]].values)
    db=DBSCAN(
        eps=DBSCAN_EPS_METERS/6371000,
        min_samples=2,
        metric="haversine"
    ).fit(coords)

    df["cluster"]=db.labels_


    return df.groupby("cluster").mean(numeric_only=True).reset_index()
    #return df.loc[df.groupby("cluster")["score"].idxmax()]  
