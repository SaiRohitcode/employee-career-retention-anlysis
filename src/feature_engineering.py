import numpy as np

def create_career_features(df):
    df = df.copy()

    company_years = df["YearsAtCompany"].replace(0, np.nan)

    df["PromotionGapRatio"] = (
        df["YearsSinceLastPromotion"] / company_years
    ).fillna(0)

    df["RoleStagnationIndex"] = (
        df["YearsInCurrentRole"] / company_years
    ).fillna(0)

    df["TrainingIntensityScore"] = (
        df["TrainingTimesLastYear"] / company_years
    ).fillna(0)

    df["ManagerStabilityIndicator"] = (
        df["YearsWithCurrManager"] / company_years
    ).fillna(0)

    return df