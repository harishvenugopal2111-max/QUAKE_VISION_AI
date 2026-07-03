import pandas as pd


def classify_risk(magnitude):

    if pd.isna(magnitude):
        return "Unknown"

    if magnitude >= 7:
        return "🔴 Extreme"

    elif magnitude >= 5:
        return "🟠 High"

    elif magnitude >= 3:
        return "🟡 Moderate"

    else:
        return "🟢 Low"


def get_country(place):

    if pd.isna(place):
        return "Unknown"

    try:
        return place.split(",")[-1].strip()
    except:
        return "Unknown"


def format_dataframe(df):

    df = df.copy()

    df["Country"] = df["Place"].apply(get_country)

    df["Risk"] = df["Magnitude"].apply(classify_risk)

    return df


def summary(df):

    return {
        "total": len(df),
        "average_magnitude": round(df["Magnitude"].mean(),2),
        "maximum_magnitude": round(df["Magnitude"].max(),2),
        "average_depth": round(df["Depth (km)"].mean(),2),
        "countries": df["Place"]
                    .apply(get_country)
                    .nunique()
    }


def strong_earthquakes(df):

    return df[df["Magnitude"] >= 5]


def recent_earthquakes(df):

    return df.sort_values(
        "Time",
        ascending=False
    )


def top10(df):

    return (
        df.sort_values(
            "Magnitude",
            ascending=False
        )
        .head(10)
    )