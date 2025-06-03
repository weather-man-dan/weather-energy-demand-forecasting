import pandas as pd

def create_features(df):
    df = df.copy()

    # 📆 Extract month number and string for seasonal analysis
    df["month_num"] = df["month"].dt.month
    df["month_str"] = df["month"].dt.strftime("%b")

    # ⏳ Lag features: previous month HDD and gas demand
    df["HDD_lag1"] = df["HDD"].shift(1)
    df["gas_demand_lag1"] = df["gas_demand"].shift(1)

    # 📉 Change in HDD from previous month
    df["HDD_diff"] = df["HDD"] - df["HDD_lag1"]

    # 🔁 Rolling average of HDD over the last 3 months
    df["HDD_rolling3"] = df["HDD"].rolling(window=3).mean()

    # 🧹 Drop any rows with missing values from lag/rolling ops
    df = df.dropna(subset=["HDD_lag1", "gas_demand_lag1", "HDD_diff", "HDD_rolling3"])
    df = df.reset_index(drop=True)

    return df


