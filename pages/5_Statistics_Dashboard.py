import streamlit as st
import pandas as pd
import plotly.express as px


st.title("📊 HPA Expression Statistics Dashboard")


@st.cache_data
def load_data():
    return pd.read_parquet("HPA_expression.parquet")


df = load_data()


st.markdown(
"""
## Dataset Overview

Statistical summary of Human Protein Atlas
gene expression data using nTPM values.
"""
)


# Summary cards

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Genes",
        df["Gene name"].nunique()
    )


with col2:
    st.metric(
        "Total Records",
        len(df)
    )


with col3:
    st.metric(
        "Average nTPM",
        round(df["nTPM"].mean(),2)
    )


with col4:
    st.metric(
        "Maximum nTPM",
        round(df["nTPM"].max(),2)
    )


# Expression distribution

st.subheader("📈 nTPM Expression Distribution")


fig1 = px.histogram(
    df,
    x="nTPM",
    nbins=50,
    title="Distribution of Gene Expression Levels"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)



# Normal vs Cancer comparison

st.subheader("🧬 Normal Tissue vs Cancer Cell Line")


comparison = (
    df.groupby("Type")["nTPM"]
    .mean()
    .reset_index()
)


fig2 = px.bar(
    comparison,
    x="Type",
    y="nTPM",
    color="Type",
    title="Average nTPM Comparison"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# Highest expressed genes

st.subheader("🔥 Top 10 Highly Expressed Genes")


top_genes = (
    df.groupby("Gene name")["nTPM"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


fig3 = px.bar(
    top_genes,
    x="Gene name",
    y="nTPM",
    title="Top Expressed Genes"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)