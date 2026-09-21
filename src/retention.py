def calculate_retention_score(df):
    df = df.copy()

    df["RetentionScore"] = (
        df["JobSatisfaction"]
        + df["EnvironmentSatisfaction"]
        + df["JobInvolvement"]
        + df["RelationshipSatisfaction"]
    )

    df["RetentionRisk"] = "Low"

    df.loc[
        df["RetentionScore"] <= 8,
        "RetentionRisk"
    ] = "Medium"

    df.loc[
        df["RetentionScore"] <= 5,
        "RetentionRisk"
    ] = "High"

    df["SuggestedAction"] = "Regular career discussion"

    df.loc[
        df["RetentionRisk"] == "Medium",
        "SuggestedAction"
    ] = "Training and career mentoring"

    df.loc[
        df["RetentionRisk"] == "High",
        "SuggestedAction"
    ] = "Rotation, promotion review and mentoring"

    return df