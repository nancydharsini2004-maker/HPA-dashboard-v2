import streamlit as st
import pandas as pd
import plotly.express as px


st.title("🧬 Normal Tissue vs Cancer Cell Line Analysis")


@st.cache_data
def load_data():
    return pd.read_parquet(
        "HPA_expression.parquet"
    )


df = load_data()


# Select gene

gene = st.selectbox(
    "Select Gene",
    sorted(df["Gene name"].dropna().unique())
)


gene_data = df[
    df["Gene name"] == gene
]


# Compare groups

comparison = (
    gene_data
    .groupby("Type")["nTPM"]
    .mean()
    .reset_index()
)


# Display values

col1, col2, col3 = st.columns(3)


normal_value = comparison[
    comparison["Type"]=="Normal Tissue"
]["nTPM"].values


cancer_value = comparison[
    comparison["Type"]=="Cancer Cell Line"
]["nTPM"].values


normal_value = normal_value[0] if len(normal_value)>0 else 0
cancer_value = cancer_value[0] if len(cancer_value)>0 else 0


with col1:
    st.metric(
        "Normal Tissue nTPM",
        round(normal_value,2)
    )


with col2:
    st.metric(
        "Cancer nTPM",
        round(cancer_value,2)
    )


with col3:

    if normal_value != 0:
        fold = cancer_value / normal_value
    else:
        fold = 0

    st.metric(
        "Fold Change",
        round(fold,2)
    )


# Chart

fig = px.bar(
    comparison,
    x="Type",
    y="nTPM",
    color="Type",
    title=f"{gene} Expression Comparison"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Detailed Data")

st.dataframe(
    gene_data.head(200)
)