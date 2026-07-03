import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="QuakeVision AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>

.main{
    background-color:#0B1220;
}

.title{
    font-size:55px;
    font-weight:700;
    color:white;
}

.subtitle{
    font-size:22px;
    color:#B8C1CC;
}

.card{
    background:#162032;
    padding:20px;
    border-radius:15px;
    color:white;
    border:1px solid #25344D;
}

.metric{
    font-size:40px;
    font-weight:bold;
    color:#4FC3F7;
}

</style>
""",unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🌍 QuakeVision AI")

st.sidebar.info("""
Real-Time Earthquake Intelligence Platform

Version : 1.0
""")

# -------------------------------
# Title
# -------------------------------
st.markdown(
'<p class="title">🌍 QuakeVision AI</p>',
unsafe_allow_html=True
)

st.markdown(
'<p class="subtitle">Real-Time Earthquake Intelligence Platform</p>',
unsafe_allow_html=True
)

st.divider()

# -------------------------------
# KPI Cards
# -------------------------------
c1,c2,c3,c4=st.columns(4)

with c1:
    st.markdown("""
    <div class="card">
    <h4>🌍 Earthquakes Today</h4>
    <p class="metric">--</p>
    </div>
    """,unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <h4>🚨 Strong Quakes</h4>
    <p class="metric">--</p>
    </div>
    """,unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h4>📍 Countries</h4>
    <p class="metric">--</p>
    </div>
    """,unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card">
    <h4>📊 Largest Magnitude</h4>
    <p class="metric">--</p>
    </div>
    """,unsafe_allow_html=True)

st.divider()

st.info("🚀 Live earthquake data will be displayed after connecting to the USGS API.")

st.success("✅ Dashboard Initialized Successfully")