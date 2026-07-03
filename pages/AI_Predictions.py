import streamlit as st
import pandas as pd
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="AI Predictions",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Earthquake Insights")

@st.cache_data(ttl=60)
def load():
    return get_live_earthquakes()

df = load()

if df.empty:
    st.error("No Live Data Available")
    st.stop()

# ---------------- KPI ----------------

total = len(df)
avg_mag = round(df["Magnitude"].mean(),2)
max_mag = round(df["Magnitude"].max(),2)

highest = df.loc[df["Magnitude"].idxmax()]

c1,c2,c3=st.columns(3)

c1.metric("Average Magnitude",avg_mag)
c2.metric("Maximum Magnitude",max_mag)
c3.metric("Today's Earthquakes",total)

st.divider()

# ---------------- AI Summary ----------------

st.subheader("🧠 AI Generated Summary")

if avg_mag < 3:
    risk="🟢 Low Global Activity"
elif avg_mag <5:
    risk="🟡 Moderate Global Activity"
elif avg_mag <7:
    risk="🟠 High Global Activity"
else:
    risk="🔴 Extreme Global Activity"

st.success(f"""
Current Global Seismic Activity : **{risk}**

Average Magnitude : **{avg_mag}**

Largest Earthquake : **{max_mag}**

Most Significant Event :

**{highest['Place']}**

Magnitude : **{highest['Magnitude']}**

Depth : **{highest['Depth (km)']} km**
""")

st.divider()

# ---------------- Strong Earthquakes ----------------

st.subheader("🚨 Strong Earthquakes")

strong=df[df["Magnitude"]>=5]

if strong.empty:
    st.info("No Strong Earthquakes Today.")
else:
    st.dataframe(
        strong,
        width="stretch"
    )

st.divider()

# ---------------- Recommendation ----------------

st.subheader("🤖 AI Recommendation")

if max_mag>=7:
    st.error("""
Extreme Earthquake Activity Detected

Recommended Action

• Monitor official disaster agencies

• Watch tsunami alerts

• Avoid affected regions
""")

elif max_mag>=5:

    st.warning("""
Moderate Seismic Activity

Recommended Action

• Monitor updates

• Track aftershocks

• Stay prepared
""")

else:

    st.success("""
Normal Seismic Activity

No major global earthquake threat detected at the moment.
""")