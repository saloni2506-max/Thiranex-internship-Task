import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Point directly to your saved Excel file path
EXCEL_FILE = "c:/Users/desai/Downloads/sales_data.xlsx"

# Load the data
try:
    df = pd.read_excel(EXCEL_FILE)
except Exception as e:
    st.error(
        f"Could not find the Excel file. Please make sure it is saved at: {EXCEL_FILE}"
    )
    st.stop()

# Ensure date formatting
df["Date"] = pd.to_datetime(df["Date"])

# 2. Streamlit Application Interface
st.set_page_config(
    page_title="Sales & Revenue Analysis Dashboard", layout="wide"
)
st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("---")

# ---- SIDEBAR FILTERS ----
st.sidebar.header("Filter Options")

# Region Filter
regions = st.sidebar.multiselect(
    "Select Region", options=df["Region"].unique(), default=df["Region"].unique()
)

# Apply Filters
filtered_df = df[df["Region"].isin(regions)]

# ---- KPI CARDS ----
total_revenue = filtered_df["Revenue"].sum()
total_units = filtered_df["Quantity"].sum()

kpi1, kpi2 = st.columns(2)
with kpi1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with kpi2:
    st.metric(label="Total Units Sold", value=f"{total_units:,}")

st.markdown("---")

# ---- CHARTS ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Revenue by Product")
    fig_product = px.bar(
        filtered_df, x="Product", y="Revenue", color="Product", barmode="group"
    )
    st.plotly_chart(fig_product, use_container_width=True)

with col2:
    st.subheader("📋 Raw Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)
    