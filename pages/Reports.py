import streamlit as st
import pandas as pd
from utils.api import get_live_earthquakes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Earthquake Reports")

@st.cache_data(ttl=60)
def load_data():
    return get_live_earthquakes()

df = load_data()

if df.empty:
    st.error("No earthquake data available.")
    st.stop()

# ---------------- Summary ----------------

st.subheader("📊 Report Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Earthquakes", len(df))
c2.metric("Average Magnitude", round(df["Magnitude"].mean(),2))
c3.metric("Maximum Magnitude", round(df["Magnitude"].max(),2))
c4.metric("Countries", df["Place"].dropna().str.split(",").str[-1].str.strip().nunique())

st.divider()

# ---------------- Table ----------------

st.subheader("Live Data")

st.dataframe(df, width="stretch")

# ---------------- CSV ----------------

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "earthquake_report.csv",
    "text/csv"
)

# ---------------- PDF ----------------

def create_pdf(data):

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    c = canvas.Canvas(temp.name, pagesize=letter)

    c.setFont("Helvetica-Bold",16)
    c.drawString(50,750,"QuakeVision AI Report")

    c.setFont("Helvetica",12)

    c.drawString(50,720,f"Total Earthquakes : {len(data)}")
    c.drawString(50,700,f"Average Magnitude : {round(data['Magnitude'].mean(),2)}")
    c.drawString(50,680,f"Maximum Magnitude : {round(data['Magnitude'].max(),2)}")

    y=640

    c.drawString(50,y,"Top 10 Earthquakes")

    y-=20

    top=data.sort_values(
        "Magnitude",
        ascending=False
    ).head(10)

    for _,row in top.iterrows():

        text=f"{row['Magnitude']} | {row['Place']}"

        c.drawString(50,y,text)

        y-=18

        if y<80:
            c.showPage()
            y=750

    c.save()

    return temp.name

pdf=create_pdf(df)

with open(pdf,"rb") as file:

    st.download_button(
        "📄 Download PDF Report",
        file,
        "earthquake_report.pdf",
        "application/pdf"
    )

os.remove(pdf)