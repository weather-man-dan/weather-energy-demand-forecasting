# This file will contain functions to clean, merge, and transform data

import pandas as pd

def merge_and_clean_data(df_weather: pd.DataFrame, df_energy: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(df_weather, df_energy, on="date")
    df = df.dropna()
    return df

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    # Rolling average of HDD
    df["HDD_rolling"] = df["HDD"].rolling(window=7).mean()

    # Lag of demand (previous day)
    df["lag_demand"] = df["demand"].shift(1)

    # Day of week (0 = Monday, 6 = Sunday)
    df["day_of_week"] = df["date"].dt.dayofweek

    # HDD difference from previous day
    df["HDD_diff"] = df["HDD"].diff()

    # Weekend flag
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Rolling average of demand (7 days)
    df["demand_rolling"] = df["demand"].rolling(window=7).mean()

    # Drop rows with NA introduced by rolling, lag, diff
    df = df.dropna()

    return df

