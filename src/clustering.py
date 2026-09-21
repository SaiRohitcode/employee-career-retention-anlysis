from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


career_features = [
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "JobLevel",
    "TotalWorkingYears",
    "YearsWithCurrManager",
    "TrainingTimesLastYear",
    "PromotionGapRatio",
    "RoleStagnationIndex",
    "TrainingIntensityScore",
    "ManagerStabilityIndicator"
]


def perform_clustering(df, n_clusters=4):
    df = df.copy()

    X = df[career_features].copy()

    X = X.replace([float("inf"), float("-inf")], 0)
    X = X.fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means clustering
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    df["CareerCluster"] = kmeans.fit_predict(X_scaled)

    # Silhouette score
    if len(set(df["CareerCluster"])) > 1:
        silhouette = silhouette_score(
            X_scaled,
            df["CareerCluster"]
        )
    else:
        silhouette = 0

    # Cluster profiles
    cluster_profile = (
        df.groupby("CareerCluster")[career_features]
        .mean()
        .round(2)
    )

    # Hierarchical clustering validation
    hierarchical = AgglomerativeClustering(
        n_clusters=n_clusters
    )

    hierarchical_labels = hierarchical.fit_predict(X_scaled)

    return (
        df,
        scaler,
        kmeans,
        silhouette,
        cluster_profile,
        hierarchical_labels
    )