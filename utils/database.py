import sqlite3
import pandas as pd

DB_NAME = "database/earthquake.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes(
            time TEXT,
            place TEXT,
            magnitude REAL,
            depth REAL,
            latitude REAL,
            longitude REAL,
            status TEXT,
            type TEXT,
            tsunami INTEGER,
            url TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_data(df):
    conn = sqlite3.connect(DB_NAME)

    df.columns = [
        "time",
        "place",
        "magnitude",
        "depth",
        "longitude",
        "latitude",
        "status",
        "type",
        "tsunami",
        "url"
    ]

    df.to_sql(
        "earthquakes",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


def load_data():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql(
        "SELECT * FROM earthquakes",
        conn
    )

    conn.close()

    return df