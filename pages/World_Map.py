import streamlit as st
import pydeck as pdk
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="World Earthquake Map",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Live Earthquake World Map")

@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("Unable to fetch earthquake data.")
    st.stop()

st.success(f"Showing {len(df)} Live Earthquakes")

# Remove missing values
df = df.dropna(subset=["Latitude","Longitude","Magnitude"])

# Radius based on Magnitude
df["radius"] = df["Magnitude"] * 15000

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[Longitude, Latitude]',
    get_radius="radius",
    get_fill_color='[255, 0, 0, 160]',
    pickable=True,
)

view = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.2,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    tooltip={
        "html": """
        <b>Magnitude:</b> {Magnitude}<br/>
        <b>Place:</b> {Place}<br/>
        <b>Depth:</b> {Depth (km)} km
        """
    }
)

st.pydeck_chart(deck)

st.divider()

st.subheader("Latest Earthquakes")

st.dataframe(df)