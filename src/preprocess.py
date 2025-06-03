# This file will contain functions to clean, merge, and transform data

import pandas as pd

def merge_and_clean_data(df_weather: pd.DataFrame, df_energy: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(df_weather, df_energy, on="date")
    df = df.dropna()
    return df

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Extract month as a categorical variable
    df["month_num"] = df["month"].dt.month
    df["month_str"] = df["month"].dt.strftime("%b")
    
    # 2. Lag features (previous month's HDD/gas demand)
    df["HDD_lag1"] = df["HDD"].shift(1)
    df["gas_demand_lag1"] = df["gas_demand"].shift(1)
    
    # 3. Optional: Rolling average of HDD (last 3 months)
    df["HDD_rolling3"] = df["HDD"].rolling(3).mean()
    
    # 4. Drop any rows with NA from lagging/rolling
    df = df.dropna().reset_index(drop=True)
    
    # 5 HDD difference from previous day
    df["HDD_diff"] = df["HDD"].diff()

    return df

