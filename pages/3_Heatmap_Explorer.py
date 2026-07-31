import streamlit as st
import pandas as pd
import plotly.express as px


st.title("🔥 Gene Expression Heatmap Explorer")


@st.cache_data
def load_data():
    return pd.read_parquet(
        "HPA_expression.parquet"
    )


df = load_data()


st.write(
    "This heatmap shows average nTPM expression "
    "of highly expressed genes across samples."
)


# Select number of genes

number = st.slider(
    "Select number of top genes",
    5,
    20,
    10
)


# Find top expressed genes

top_genes = (
    df.groupby("Gene name")["nTPM"]
    .mean()
    .sort_values(ascending=False)
    .head(number)
    .index
)


heatmap_data = df[
    df["Gene name"].isin(top_genes)
]


# Create matrix

matrix = (
    heatmap_data
    .groupby(["Gene name", "Sample"])["nTPM"]
    .mean()
    .reset_index()
)


pivot = matrix.pivot(
    index="Gene name",
    columns="Sample",
    values="nTPM"
)


# Limit columns because dataset is huge

pivot = pivot.iloc[:, :50]


fig = px.imshow(
    pivot,
    labels={
        "x":"Sample",
        "y":"Gene",
        "color":"nTPM"
    },
    title="Gene Expression Heatmap",
    color_continuous_scale="Reds"

)


st.plotly_chart(
    fig,
    use_container_width=True
)