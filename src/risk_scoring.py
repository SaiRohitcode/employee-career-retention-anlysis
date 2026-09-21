def calculate_promotion_risk(df):
    df = df.copy()

    df["PromotionRiskScore"] = (
        df["YearsSinceLastPromotion"] * 2
        + df["YearsInCurrentRole"]
        + df["RoleStagnationIndex"] * 5
    )

    medium_threshold = df["PromotionRiskScore"].quantile(0.50)
    high_threshold = df["PromotionRiskScore"].quantile(0.75)

    df["PromotionRiskLevel"] = "Low"

    df.loc[
        df["PromotionRiskScore"] >= medium_threshold,
        "PromotionRiskLevel"
    ] = "Medium"

    df.loc[
        df["PromotionRiskScore"] >= high_threshold,
        "PromotionRiskLevel"
    ] = "High"

    return df, medium_threshold, high_threshold