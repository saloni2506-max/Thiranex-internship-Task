import os
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import streamlit as st

# 1. Point directly to your saved Excel dataset
EXCEL_FILE = "c:/Users/desai/Downloads/customer_data.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error(f"Cannot find data file at {EXCEL_FILE}. Please check Step 1.")
    st.stop()

df = pd.read_excel(EXCEL_FILE)

# 2. Machine Learning: K-Means Clustering Setup
# We are creating 3 groups/clusters of customers based on Age and Spending Score
features = df[["Age", "Spending_Score"]]
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(features)

# Convert clusters into readable names
cluster_map = {
    0: "Target Group (High Spending)",
    1: "Thrifty Group (Low Spending)",
    2: "Balanced Spenders",
}
df["Customer Segment"] = df["Cluster"].map(cluster_map)

# 3. Streamlit Interface UI Layout
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("👥 Customer Segmentation Dashboard (AI Clustering)")
st.markdown("---")

# ---- SIDEBAR FILTER ----
st.sidebar.header("Filter Segment View")
chosen_segment = st.sidebar.multiselect(
    "Select Customer Segments",
    options=df["Customer Segment"].unique(),
    default=df["Customer Segment"].unique(),
)

filtered_df = df[df["Customer Segment"].isin(chosen_segment)]

# ---- MAIN INTERFACE DISPLAYS ----
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Cluster Scatter Plot (AI Groups)")
    # Visualizing how the AI separated the customers
    fig_scatter = px.scatter(
        filtered_df,
        x="Age",
        y="Spending_Score",
        color="Customer Segment",
        size="Annual_Income_k",
        hover_data=["Customer_ID", "Gender"],
        title="Customers Grouped by Age and Spending Habits",
        template="plotly_white",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader("📈 Segment Population Counts")
    segment_counts = (
        filtered_df["Customer Segment"].value_counts().reset_index()
    )
    fig_pie = px.pie(
        segment_counts,
        values="count",
        names="Customer Segment",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.subheader("📋 Segmented Customer Directory Data")
st.dataframe(filtered_df, use_container_width=True)
