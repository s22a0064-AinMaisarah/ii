import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📊 Traffic Disagreement Dashboard")

    data_url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/DisagreementTraffic/main/merged_data.csv"
    df = pd.read_csv(data_url)

    st.success("Dataset loaded successfully")

    area = st.selectbox("Select Area Type", df["Area Type"].unique())

    filtered = df[df["Area Type"] == area]

    factor_cols = [c for c in df.columns if "Factor" in c]

    counts = filtered[factor_cols].isin([1,2]).sum().reset_index()
    counts.columns = ["Factor", "Disagreement Count"]

    fig = px.bar(counts, x="Disagreement Count", y="Factor", orientation="h")

    st.plotly_chart(fig, use_container_width=True)
