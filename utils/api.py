import requests
import pandas as pd

# USGS Earthquake API (Past 24 Hours)
USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


def get_live_earthquakes():
    """
    Fetch live earthquake data from USGS API
    Returns a pandas DataFrame
    """

    try:
        response = requests.get(USGS_URL, timeout=10)
        response.raise_for_status()

        data = response.json()

        earthquakes = []

        for feature in data["features"]:

            properties = feature["properties"]
            geometry = feature["geometry"]

            earthquakes.append({
                "Time": properties.get("time"),
                "Place": properties.get("place"),
                "Magnitude": properties.get("mag"),
                "Depth (km)": geometry["coordinates"][2],
                "Longitude": geometry["coordinates"][0],
                "Latitude": geometry["coordinates"][1],
                "Status": properties.get("status"),
                "Type": properties.get("type"),
                "Tsunami": properties.get("tsunami"),
                "URL": properties.get("url")
            })

        df = pd.DataFrame(earthquakes)

        # Convert timestamp
        df["Time"] = pd.to_datetime(df["Time"], unit="ms")

        return df

    except Exception as e:
        print("API Error:", e)
        return pd.DataFrame()