import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def app():
    st.title("📊 Traffic Disagreement Dashboard")

    # Load Data
    data_url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/ii/refs/heads/main/cleaned_data.csv"
    df = pd.read_csv(data_url)

    # --- FIX 1: Define the column groups explicitly ---
    factor_cols = [c for c in df.columns if "Factor" in c]
    effect_cols = [c for c in df.columns if "Effect" in c]
    step_cols   = [c for c in df.columns if "Step" in c]
    all_likert_cols = factor_cols + effect_cols + step_cols

    heatmap_data_detailed = []

    # --- FIX 2: Use 'df' instead of 'merged_df' ---
    for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
        # Ensure the area exists in your data to avoid empty slices
        if area in df["Area Type"].unique():
            for col in all_likert_cols:
                # Filter by current area
                area_filter = df[df['Area Type'] == area]
                count_sd = area_filter[col].isin([1]).sum()
                count_d  = area_filter[col].isin([2]).sum()
                total_disagreement_count = count_sd + count_d

                if total_disagreement_count > 0:
                    heatmap_data_detailed.append({
                        'Area Type': area,
                        'Likert Item': col,
                        'Total Disagreement Count': total_disagreement_count,
                        'Strongly Disagree (1)': count_sd,
                        'Disagree (2)': count_d,
                        'Category': ('Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step')
                    })

    if not heatmap_data_detailed:
        st.warning("No disagreement data (values 1 or 2) found in the dataset.")
        return

    heatmap_df_detailed = pd.DataFrame(heatmap_data_detailed)

    # Pivot logic
    heatmap_pivot_z = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
    heatmap_pivot_sd = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
    heatmap_pivot_d = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

    # Prepare customdata for hover effects
    # We stack SD and D values so they are accessible in the hovertemplate
    customdata_array = np.dstack((heatmap_pivot_sd.values, heatmap_pivot_d.values))

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot_z.values,
        x=heatmap_pivot_z.columns,
        y=heatmap_pivot_z.index,
        colorscale='YlGnBu',
        text=heatmap_pivot_z.values,
        texttemplate="%{text}",
        customdata=customdata_array,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total: %{z}<br>Strongly Disagree: %{customdata[0]}<br>Disagree: %{customdata[1]}<extra></extra>'
    ))

    fig.update_layout(height=800, title="Disagreement Distribution")
    
    # --- FIX 3: Use st.plotly_chart instead of fig.show() ---
    st.plotly_chart(fig, use_container_width=True)
