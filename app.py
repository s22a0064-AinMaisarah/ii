import streamlit as st
import GoogleFormData
import TrafficDashboard

st.set_page_config(
    page_title="Traffic Analytics Dashboard",
    layout="wide"
)

st.sidebar.title("🚦 Traffic Analytics Dashboard")

page = st.sidebar.radio(
    "Navigate",
    ["Google Form Data", "Traffic Dashboard"]
)

if page == "Google Form Data":
    GoogleFormData.app()

elif page == "Traffic Dashboard":
    TrafficDashboard.app()
