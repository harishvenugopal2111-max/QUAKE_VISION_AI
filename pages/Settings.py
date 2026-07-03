import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings")

st.subheader("Application")

refresh = st.selectbox(
    "Auto Refresh",
    [
        "30 Seconds",
        "1 Minute",
        "5 Minutes",
        "Disabled"
    ]
)

theme = st.selectbox(
    "Theme",
    [
        "Dark",
        "Light"
    ]
)

st.divider()

st.subheader("API Status")

url="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

try:
    r=requests.get(url,timeout=5)

    if r.status_code==200:
        st.success("🟢 USGS API Online")
    else:
        st.error("🔴 API Offline")

except:
    st.error("🔴 Unable to Connect")

st.divider()

st.subheader("Application Information")

st.write("Project : QuakeVision AI")

st.write("Version : 1.0")

st.write("Developer : Harish Venugopal")

st.write(
    "Last Checked :",
    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

st.divider()

if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache Cleared Successfully")