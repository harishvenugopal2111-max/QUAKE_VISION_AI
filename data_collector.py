from utils.api import get_live_earthquakes
from utils.database import save_data

def collect_data():
    df = get_live_earthquakes()

    if not df.empty:
        save_data(df)
        print(f"Saved {len(df)} records.")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    collect_data()