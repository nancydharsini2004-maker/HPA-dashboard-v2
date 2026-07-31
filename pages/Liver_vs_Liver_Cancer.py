import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Liver Tissue vs Liver Cancer",
    page_icon="🫀",
    layout="wide"
)


# Load data

@st.cache_data
def load_data():
    return pd.read_parquet("HPA_expression.parquet")


df = load_data()


st.title("🫀 Liver Tissue vs Liver Cancer Cell Line")


st.markdown(
"""
## Biological Comparison

This section compares gene expression patterns between:

🟢 **Normal Liver Tissue**

and

🔴 **Liver Cancer Cell Lines**

Expression measurement:
**nTPM (normalized Transcripts Per Million)**

The analysis highlights genes with different
transcriptomic activity between healthy and cancer conditions.
"""
)


# Check available samples

st.sidebar.header("🔬 Select Cancer Cell Line")


# Normal liver

normal_liver = df[
    (df["Type"] == "Normal Tissue") &
    (df["Sample"].str.lower() == "liver")
]


st.subheader("🟢 Normal Liver Tissue")


if len(normal_liver) == 0:

    st.warning(
        "Normal liver tissue was not found. Check sample names."
    )

else:

    liver_genes = (
        normal_liver
        .groupby("Gene name")["nTPM"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


    fig1 = px.bar(
        liver_genes,
        x="Gene name",
        y="nTPM",
        title="Top 10 Expressed Genes in Normal Liver",
        color="nTPM"
    )


    st.plotly_chart(
        fig1,
        use_container_width=True
    )



# Cancer cell line

cancer = df[
    df["Type"] == "Cancer Cell Line"
]


cell_line = st.sidebar.selectbox(
    "Choose Cancer Cell Line",
    sorted(
        cancer["Sample"]
        .dropna()
        .unique()
    )
)


cancer_selected = cancer[
    cancer["Sample"] == cell_line
]


st.subheader(
    f"🔴 Liver Cancer Cell Line: {cell_line}"
)


cancer_genes = (
    cancer_selected
    .groupby("Gene name")["nTPM"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


fig2 = px.bar(
    cancer_genes,
    x="Gene name",
    y="nTPM",
    title=f"Top 10 Expressed Genes in {cell_line}",
    color="nTPM"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# Comparison section

st.subheader("📊 Expression Summary")


col1, col2 = st.columns(2)


with col1:
    st.metric(
        "Normal Liver Average nTPM",
        round(
            normal_liver["nTPM"].mean(),
            2
        )
    )


with col2:
    st.metric(
        "Cancer Cell Line Average nTPM",
        round(
            cancer_selected["nTPM"].mean(),
            2
        )
    )


st.success(
"""
This comparison helps identify transcriptomic
changes between healthy liver tissue and cancer
cell line models.
"""
)