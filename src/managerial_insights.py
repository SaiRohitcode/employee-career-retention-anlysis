def generate_insights(df):
    insights = []

    high_gap = (
        df["PromotionRiskLevel"] == "High"
    ).sum()

    high_retention = (
        df["RetentionRisk"] == "High"
    ).sum()

    stagnant_roles = (
        df.groupby("JobRole")["RoleStagnationIndex"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )

    insights.append(
        f"Employees with high promotion risk: {high_gap}"
    )

    insights.append(
        f"Employees with high retention risk: {high_retention}"
    )

    insights.append(
        "Roles with high stagnation"
    )

    for role, score in stagnant_roles.items():
        insights.append(
            f"{role}: {score:.2f}"
        )

    return insights