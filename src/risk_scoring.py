def calculate_promotion_risk(df):
    df = df.copy()
    df["PromotionRiskScore"] = (
        df["YearsSinceLastPromotion"] * 2
        + df["YearsInCurrentRole"]
        + df["RoleStagnationIndex"] * 5
    )
    df["PromotionRiskLevel"] = "Low"
    df.loc[df["PromotionRiskScore"] >= 15, "PromotionRiskLevel"] = "Medium"
    df.loc[df["PromotionRiskScore"] >= 30, "PromotionRiskLevel"] = "High"
    return df