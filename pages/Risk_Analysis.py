import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import get_live_earthquakes

st.set_page_config(
    page_title="Risk Analysis",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Earthquake Risk Analysis")

@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("No live earthquake data found.")
    st.stop()

# -----------------------------
# Risk Classification
# -----------------------------
def classify_risk(mag):
    if mag >= 7:
        return "🔴 Extreme"
    elif mag >= 5:
        return "🟠 High"
    elif mag >= 3:
        return "🟡 Moderate"
    else:
        return "🟢 Low"

df["Risk"] = df["Magnitude"].fillna(0).apply(classify_risk)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

risk = st.sidebar.multiselect(
    "Select Risk Level",
    df["Risk"].unique(),
    default=df["Risk"].unique()
)

filtered = df[df["Risk"].isin(risk)]

# -----------------------------
# KPI
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Events", len(filtered))
c2.metric("Extreme", len(filtered[filtered["Risk"]=="🔴 Extreme"]))
c3.metric("High", len(filtered[filtered["Risk"]=="🟠 High"]))
c4.metric("Moderate", len(filtered[filtered["Risk"]=="🟡 Moderate"]))

st.divider()

# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("Risk Distribution")

risk_count = (
    filtered["Risk"]
    .value_counts()
    .reset_index()
)

risk_count.columns = ["Risk", "Count"]

fig = px.pie(
    risk_count,
    names="Risk",
    values="Count",
    hole=0.5
)

st.plotly_chart(fig, width="stretch")

# -----------------------------
# Bar Chart
# -----------------------------
st.subheader("Risk Level Count")

fig2 = px.bar(
    risk_count,
    x="Risk",
    y="Count",
    color="Risk"
)

st.plotly_chart(fig2, width="stretch")

# -----------------------------
# High Risk Table
# -----------------------------
st.subheader("Live Earthquake Risk Table")

st.dataframe(
    filtered,
    width="stretch"
)

# -----------------------------
# Download
# -----------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "earthquake_risk_analysis.csv",
    "text/csv"
)