# This file will contain functions to clean, merge, and transform data

import pandas as pd

def merge_and_clean_data(df_weather: pd.DataFrame, df_energy: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(df_weather, df_energy, on="date")
    df = df.dropna()
    return df

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df["HDD_rolling"] = df["HDD"].rolling(window=7).mean()
    df["lag_demand"] = df["demand"].shift(1)
    df = df.dropna()
    return df

