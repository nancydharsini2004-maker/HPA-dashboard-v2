import streamlit as st
import pandas as pd
import plotly.express as px


st.title("🔍 Gene Expression Explorer")


@st.cache_data
def load_data():
    return pd.read_parquet("HPA_expression.parquet")


df = load_data()


st.markdown(
"""
Search a gene to compare its expression
between normal tissues and cancer cell lines.
"""
)


# Gene selection

gene = st.selectbox(
    "Select Gene",
    sorted(df["Gene name"].dropna().unique())
)


gene_data = df[
    df["Gene name"] == gene
]


st.subheader(f"Expression Profile: {gene}")


# Average expression

summary = (
    gene_data
    .groupby("Type")["nTPM"]
    .mean()
    .reset_index()
)


fig = px.bar(
    summary,
    x="Type",
    y="nTPM",
    color="Type",
    title=f"{gene} Normal vs Cancer Expression"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# Show data

st.subheader("Gene Data")

st.dataframe(
    gene_data,
    use_container_width=True
)