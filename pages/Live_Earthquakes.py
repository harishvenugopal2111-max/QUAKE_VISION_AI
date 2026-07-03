import streamlit as st
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="Live Earthquakes",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Live Earthquakes")

@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("Unable to fetch live earthquake data.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")

min_mag = st.sidebar.slider(
    "Minimum Magnitude",
    0.0,
    10.0,
    0.0
)

filtered = df[df["Magnitude"] >= min_mag]

# KPIs
c1, c2, c3 = st.columns(3)

c1.metric("Total Earthquakes", len(filtered))
c2.metric("Strong Quakes (5+)", len(filtered[filtered["Magnitude"] >= 5]))
c3.metric("Largest Magnitude", round(filtered["Magnitude"].max(), 2))

st.divider()

st.dataframe(
    filtered,
    use_container_width=True
)