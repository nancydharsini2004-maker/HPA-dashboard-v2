import streamlit as st
import pandas as pd
import plotly.express as px


# Page settings
st.set_page_config(
    page_title="Comparative Gene Expression Analysis Using Human Protein Atlas",
    page_icon="🧬",
    layout="wide"
)


# Load dataset
@st.cache_data
def load_data():
    df = pd.read_parquet("HPA_expression.parquet")
    return df


df = load_data()


# Sidebar design

st.markdown("""
### Comparative Analysis of Gene Expression Between Normal Human Tissue and Cancer Cell Lines

This dashboard enables interactive exploration and comparison of transcriptomic gene expression (nTPM)
between normal tissues and tissue-specific cancer cell lines using Human Protein Atlas (HPA) data.
""")


st.sidebar.divider()


st.sidebar.subheader("📊 Dataset Information")

st.sidebar.write(
"""
Source:
Human Protein Atlas (HPA)

Measurement:
nTPM expression
"""
)


st.sidebar.divider()


st.sidebar.info(
"""
Navigation:

🔍 Gene Expression Explorer

🧬 Normal vs Cancer

🔥 Expression Heatmap

🫀 Liver Tissue vs Liver Cancer

📊 Statistical Analysis
"""
)


# Main dashboard title

st.title(
    "🧬 HPA Gene Expression Analysis Dashboard"
)


st.markdown(
"""
## About this Project

This interactive dashboard analyzes transcriptomic
gene expression data obtained from the **Human Protein Atlas (HPA)**.

The expression values are represented as:

### nTPM (normalized Transcripts Per Million)

The dashboard enables exploration and comparison of:

- 🟢 Normal human tissues
- 🔴 Cancer cell lines

to identify differences in gene expression patterns
through interactive visualization.
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
        "Total Expression Records",
        len(df)
    )


with col3:
    normal_count = len(
        df[df["Type"] == "Normal Tissue"]
    )

    st.metric(
        "Normal Tissue Records",
        normal_count
    )


with col4:
    cancer_count = len(
        df[df["Type"] == "Cancer Cell Line"]
    )

    st.metric(
        "Cancer Cell Line Records",
        cancer_count
    )


# Dataset preview

st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(100),
    use_container_width=True
)


# Dataset information

with st.expander("🔎 View Dataset Columns"):
    st.write(df.columns.tolist())
