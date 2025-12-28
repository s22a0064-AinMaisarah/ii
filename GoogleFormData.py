import streamlit as st
import pandas as pd

def app():
    st.title("📋 Google Form Traffic Survey Data")

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8nPPwgVKnGxpQLQFTH6EQLpO6l1l2BlEAdGqmb0Bq7FGQzViLwKbb78NMjJSA1-eHl-Ebq5Wl4LRU/pub?gid=745446698&single=true&output=csv"
    df = pd.read_csv(url)

    df = df.drop(columns=["Timestamp", "Score"], errors="ignore")

    st.metric("Total Respondents", len(df))
    st.dataframe(df)
