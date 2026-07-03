
import streamlit as st
import plotly.express as px
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="Earthquake Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Earthquake Analytics Dashboard")

@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()

df = df.dropna(subset=["Magnitude"])

# ---------------- Filters ----------------

st.sidebar.header("Filters")

min_mag = st.sidebar.slider(
    "Minimum Magnitude",
    0.0,
    10.0,
    0.0
)

filtered = df[df["Magnitude"] >= min_mag]

# ---------------- KPI ----------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Earthquakes",
    len(filtered)
)

c2.metric(
    "Average Magnitude",
    round(filtered["Magnitude"].mean(),2)
)

c3.metric(
    "Maximum Magnitude",
    round(filtered["Magnitude"].max(),2)
)

c4.metric(
    "Average Depth",
    round(filtered["Depth (km)"].mean(),2)
)

st.divider()

# ---------------- Magnitude Distribution ----------------

st.subheader("Magnitude Distribution")

fig = px.histogram(
    filtered,
    x="Magnitude",
    nbins=20,
    color="Magnitude"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- Depth Distribution ----------------

st.subheader("Depth Distribution")

fig2 = px.box(
    filtered,
    y="Depth (km)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------- Top Locations ----------------

st.subheader("Top Earthquake Locations")

top = (
    filtered["Place"]
    .value_counts()
    .head(10)
    .reset_index()
)

top.columns=["Location","Count"]

fig3 = px.bar(
    top,
    x="Location",
    y="Count",
    color="Count"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------- Timeline ----------------

st.subheader("Earthquakes Timeline")

timeline = (
    filtered
    .sort_values("Time")
)

fig4 = px.scatter(
    timeline,
    x="Time",
    y="Magnitude",
    size="Magnitude",
    hover_data=["Place"]
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.divider()

st.dataframe(filtered)