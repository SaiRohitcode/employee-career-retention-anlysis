import streamlit as st
from src.data_loader import load_data
from src.feature_engineering import create_career_features
from src.clustering import perform_clustering
from src.risk_scoring import calculate_promotion_risk
from src.retention import calculate_retention_score
from src.managerial_insights import generate_insights

st.set_page_config(page_title="Career Analytics", layout="wide")
st.title("Employee Career Development & Retention Analytics")

# Load and process data
df = load_data()
df = create_career_features(df)
df, scaler, kmeans, silhouette, cluster_profile, hierarchical_labels = perform_clustering(df)

# Calculate promotion risk
risk_result = calculate_promotion_risk(df)
df = risk_result[0] if isinstance(risk_result, tuple) else risk_result

# Calculate retention risk
df = calculate_retention_score(df)

# Sidebar filters
st.sidebar.header("Filters")
departments = ["All"] + sorted(df["Department"].dropna().unique().tolist())
department = st.sidebar.selectbox("Department", departments)

if department == "All":
    available_roles = sorted(df["JobRole"].dropna().unique().tolist())
else:
    available_roles = sorted(df.loc[df["Department"] == department, "JobRole"].dropna().unique().tolist())

role = st.sidebar.selectbox("Job Role", ["All"] + available_roles)
cluster_options = ["All"] + sorted(df["CareerCluster"].dropna().unique().tolist())
cluster = st.sidebar.selectbox("Career Cluster", cluster_options)

# Apply filters
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]

if role != "All":
    filtered_df = filtered_df[filtered_df["JobRole"] == role]

if cluster != "All":
    filtered_df = filtered_df[filtered_df["CareerCluster"] == cluster]

if filtered_df.empty:
    st.warning("No employees match the selected filters.")
    st.stop()

# Overview
st.header("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", len(filtered_df))
col2.metric("High Promotion Risk", (filtered_df["PromotionRiskLevel"] == "High").sum())
col3.metric("High Retention Risk", (filtered_df["RetentionRisk"] == "High").sum())
col4.metric("Silhouette Score", round(silhouette, 3))

# Career Path Clustering
st.header("Career Path Clustering Dashboard")
st.subheader("Cluster Distribution")
cluster_counts = filtered_df["CareerCluster"].value_counts().sort_index()
st.bar_chart(cluster_counts)

st.subheader("Career Pattern Summaries")
st.dataframe(cluster_profile, use_container_width=True)

# Promotion Gap Monitor
st.header("Promotion Gap Monitor")
max_gap = float(df["PromotionGapRatio"].max())
gap_threshold = st.slider(
    "Promotion Gap Threshold",
    min_value=0.0,
    max_value=max(1.0, max_gap),
    value=0.0,
    step=0.1
)

gap_df = filtered_df[filtered_df["PromotionGapRatio"] >= gap_threshold]
gap_columns = [
    "JobRole",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "PromotionGapRatio",
    "PromotionRiskScore",
    "PromotionRiskLevel"
]

if gap_df.empty:
    st.info("No employees meet the selected promotion gap threshold.")
else:
    st.dataframe(gap_df[gap_columns], use_container_width=True)

# Retention Opportunity Panel
st.header("Retention Opportunity Panel")
retention_df = filtered_df[filtered_df["RetentionRisk"].isin(["Medium", "High"])]

retention_columns = [
    "Department",
    "JobRole",
    "RetentionScore",
    "RetentionRisk",
    "SuggestedAction"
]

if retention_df.empty:
    st.info("No medium- or high-risk employees found.")
else:
    st.dataframe(retention_df[retention_columns], use_container_width=True)

st.subheader("Suggested Actions")

if retention_df.empty:
    st.info("No suggested actions available.")
else:
    action_counts = retention_df["SuggestedAction"].value_counts()
    st.bar_chart(action_counts)

# Managerial Insights
st.header("Managerial Insight Dashboard")
st.subheader("Manager Tenure vs Career Growth")

st.scatter_chart(
    filtered_df,
    x="YearsWithCurrManager",
    y="YearsSinceLastPromotion"
)

st.subheader("Team-Level Stagnation Signals")
team_stagnation = (
    filtered_df.groupby("Department")["RoleStagnationIndex"]
    .mean()
    .sort_values(ascending=False)
)
st.bar_chart(team_stagnation)

st.subheader("Managerial Insights")
insights = generate_insights(filtered_df)

for insight in insights:
    st.write(insight)

# Cluster Explorer
st.header("Cluster Explorer")
available_clusters = sorted(filtered_df["CareerCluster"].dropna().unique().tolist())

selected_cluster = st.selectbox("Select Cluster", available_clusters)
selected_cluster_df = filtered_df[filtered_df["CareerCluster"] == selected_cluster]

st.write(f"Employees in Cluster {selected_cluster}: {len(selected_cluster_df)}")
st.dataframe(selected_cluster_df, use_container_width=True)