import pandas as pd
from sklearn.cluster import DBSCAN

def detect_hotspots(df):

    data = df[["Latitude","Longitude"]].dropna()

    model = DBSCAN(
        eps=2,
        min_samples=5
    )

    labels = model.fit_predict(data)

    data["Cluster"] = labels

    return data