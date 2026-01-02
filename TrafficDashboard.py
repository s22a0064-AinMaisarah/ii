import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def app():
    st.title("📊 Traffic Disagreement Dashboard")

    # 1. Load Data
    data_url = "https://raw.githubusercontent.com/s22a0064-AinMaisarah/ii/refs/heads/main/cleaned_data.csv"
    try:
        df = pd.read_csv(data_url)
        st.success("Dataset loaded successfully")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # 2. Define Column Groups
    # Dynamically identifying columns based on your naming convention
    factor_cols = [c for c in df.columns if "Factor" in c]
    effect_cols = [c for c in df.columns if "Effect" in c]
    step_cols = [c for c in df.columns if "Step" in c]
    all_likert_cols = factor_cols + effect_cols + step_cols

    # 3. Prepare Heatmap Data
    heatmap_data_detailed = []
    areas = ['Rural areas', 'Suburban areas', 'Urban areas']

    for area in areas:
        for col in all_likert_cols:
            # Filter by area and count SD (1) and D (2)
            subset = df[df['Area Type'] == area]
            count_sd = subset[col].isin([1]).sum()
            count_d  = subset[col].isin([2]).sum()
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
        st.warning("No disagreement data found to display.")
        return

    heatmap_df_detailed = pd.DataFrame(heatmap_data_detailed)

    # 4. Pivot and Organize Data
    # Ensure specific ordering Factor -> Effect -> Step
    item_order = [i for i in all_likert_cols if i in heatmap_df_detailed['Likert Item'].unique()]
    heatmap_df_detailed['Likert Item'] = pd.Categorical(heatmap_df_detailed['Likert Item'], categories=item_order, ordered=True)

    heatmap_pivot_z = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Total Disagreement Count').fillna(0)
    heatmap_pivot_sd = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Strongly Disagree (1)').fillna(0)
    heatmap_pivot_d = heatmap_df_detailed.pivot(index='Likert Item', columns='Area Type', values='Disagree (2)').fillna(0)

    # Create Customdata for Hover
    customdata_array = np.stack((heatmap_pivot_sd.values, heatmap_pivot_d.values), axis=-1)

    # 5. Create Plotly Figure
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot_z.values,
        x=heatmap_pivot_z.columns,
        y=heatmap_pivot_z.index,
        colorscale='YlGnBu',
        text=heatmap_pivot_z.values,
        texttemplate="%{text}",
        showscale=True,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total Disagreement: %{z}<br>Strongly Disagree (1): %{customdata[0]}<br>Disagree (2): %{customdata[1]}<extra></extra>',
        customdata=customdata_array
    ))

    # Add grid lines
    for i in range(len(heatmap_pivot_z.index)+1):
        fig.add_shape(type='line', x0=-0.5, x1=len(heatmap_pivot_z.columns)-0.5, y0=i-0.5, y1=i-0.5, line=dict(color='white', width=2))
    for j in range(len(heatmap_pivot_z.columns)+1):
        fig.add_shape(type='line', y0=-0.5, y1=len(heatmap_pivot_z.index)-0.5, x0=j-0.5, x1=j-0.5, line=dict(color='white', width=2))

    fig.update_layout(
        title="Disagreement Responses (1 & 2) Across Area Types",
        xaxis_title="Area Type",
        yaxis_title="Likert Scale Item",
        template='plotly_white',
        height=900
    )

    # 6. Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Important: This part allows the app to run if this script is the main entry point
if __name__ == "__main__":
    app()
