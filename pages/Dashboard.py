import streamlit as st
import plotly.express as px
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="QuakeVision AI Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 QuakeVision AI")
st.caption("Real-Time Earthquake Intelligence Platform")

# ---------------- Load Data ----------------
@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("Unable to fetch live earthquake data.")
    st.stop()

# ---------------- KPIs ----------------

total = len(df)

strong = len(df[df["Magnitude"] >= 5])

largest = round(df["Magnitude"].max(), 2)

avg = round(df["Magnitude"].mean(), 2)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🌍 Total Earthquakes", total)

c2.metric("🚨 Strong Quakes", strong)

c3.metric("📈 Largest Magnitude", largest)

c4.metric("📊 Average Magnitude", avg)

st.divider()

# ---------------- Charts ----------------

left, right = st.columns(2)

with left:

    st.subheader("Magnitude Distribution")

    fig = px.histogram(
        df,
        x="Magnitude",
        nbins=20,
        color="Magnitude",
        title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Top 10 Strongest Earthquakes")

    top = (
        df.sort_values(
            "Magnitude",
            ascending=False
        )
        .head(10)
    )

    fig2 = px.bar(
        top,
        x="Magnitude",
        y="Place",
        orientation="h",
        color="Magnitude"
    )

    fig2.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ---------------- Recent Earthquakes ----------------

st.subheader("🕒 Latest Earthquakes")

latest = df.sort_values(
    "Time",
    ascending=False
)

st.dataframe(
    latest[
        [
            "Time",
            "Place",
            "Magnitude",
            "Depth (km)",
            "Status"
        ]
    ],
    use_container_width=True,
    height=400
)

st.divider()

# ---------------- AI Summary ----------------

st.subheader("🤖 AI Summary")

highest = df.loc[df["Magnitude"].idxmax()]

st.info(
    f"""
🌍 **Today's Earthquake Activity**

- Total Earthquakes: **{total}**
- Strong Earthquakes (≥5): **{strong}**
- Largest Magnitude: **{largest}**
- Average Magnitude: **{avg}**

### Strongest Earthquake
📍 **{highest['Place']}**

Magnitude: **{highest['Magnitude']}**

Depth: **{highest['Depth (km)']} km**
"""
)

st.success("✅ Dashboard Updated Successfully (Auto Refresh: 60 Seconds)")