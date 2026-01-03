import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def app():
    st.title("📊 Traffic Disagreement Dashboard")

    # Load data locally (BEST PRACTICE)
    df = pd.read_csv("cleaned_data.csv")

    factor_cols = [c for c in df.columns if "Factor" in c]
    effect_cols = [c for c in df.columns if "Effect" in c]
    step_cols   = [c for c in df.columns if "Step" in c]
    all_likert_cols = factor_cols + effect_cols + step_cols

    heatmap_data_detailed = []

    for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
        if area in df["Area Type"].unique():
            area_filter = df[df['Area Type'] == area]

            for col in all_likert_cols:
                count_sd = area_filter[col].isin([1]).sum()
                count_d  = area_filter[col].isin([2]).sum()

                total = count_sd + count_d
                if total > 0:
                    heatmap_data_detailed.append({
                        'Area Typ
