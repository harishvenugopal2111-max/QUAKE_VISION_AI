import streamlit as st
import pandas as pd
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="Earthquake Alerts",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Live Earthquake Alert Center")

@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("Unable to fetch live earthquake data.")
    st.stop()

# ---------------- Alert Level ----------------

def alert_level(mag):
    if mag >= 7:
        return "🔴 Emergency"
    elif mag >= 6:
        return "🟠 Critical"
    elif mag >= 5:
        return "🟡 Warning"
    else:
        return "🟢 Normal"

df["Alert"] = df["Magnitude"].fillna(0).apply(alert_level)

# ---------------- Sidebar ----------------

st.sidebar.header("Alert Filter")

selected = st.sidebar.multiselect(
    "Select Alert Level",
    df["Alert"].unique(),
    default=df["Alert"].unique()
)

filtered = df[df["Alert"].isin(selected)]

# ---------------- KPIs ----------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Emergency",
    len(filtered[filtered["Alert"]=="🔴 Emergency"])
)

c2.metric(
    "Critical",
    len(filtered[filtered["Alert"]=="🟠 Critical"])
)

c3.metric(
    "Warning",
    len(filtered[filtered["Alert"]=="🟡 Warning"])
)

c4.metric(
    "Total Alerts",
    len(filtered)
)

st.divider()

# ---------------- Alert Cards ----------------

st.subheader("🚨 Recent Alerts")

for _, row in filtered.head(10).iterrows():

    if row["Alert"]=="🔴 Emergency":
        st.error(
            f"""
{row['Alert']}

📍 {row['Place']}

Magnitude : {row['Magnitude']}

Depth : {row['Depth (km)']} km

Time : {row['Time']}
"""
        )

    elif row["Alert"]=="🟠 Critical":
        st.warning(
            f"""
{row['Alert']}

📍 {row['Place']}

Magnitude : {row['Magnitude']}

Depth : {row['Depth (km)']} km

Time : {row['Time']}
"""
        )

    elif row["Alert"]=="🟡 Warning":
        st.info(
            f"""
{row['Alert']}

📍 {row['Place']}

Magnitude : {row['Magnitude']}

Depth : {row['Depth (km)']} km

Time : {row['Time']}
"""
        )

st.divider()

st.subheader("📋 Alert History")

st.dataframe(
    filtered,
    width="stretch"
)

# ---------------- Download ----------------

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download Alert Report",
    csv,
    "earthquake_alerts.csv",
    "text/csv"
)