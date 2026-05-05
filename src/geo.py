import numpy as np
from sklearn.neighbors import BallTree

EARTH_RADIUS = 6371000

def haversine_distances(points_a, points_b):
    points_a=np.radians(points_a)
    points_b=np.radians(points_b)

    tree=BallTree(data=points_b, metric="haversine")

    dist,ind=tree.query(points_a, k=1)

    return dist.flatten() * EARTH_RADIUS, ind.flatten()

def count_neighbors_within(points_a, points_b, radius_m):
    tree=BallTree(np.radians(points_b), metric="haversine")
    counts=tree.query_radius(np.radians(points_a), r=radius_m/EARTH_RADIUS, count_only=True)
    return counts