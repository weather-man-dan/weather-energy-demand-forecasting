import pandas as pd
import numpy as np
import os

# -----------------------------------
# Process NOAA Weather Data
# -----------------------------------

def process_noaa(filepath):
    df = pd.read_csv(filepath)

    # Drop rows where both TMAX and TMIN are missing
    df = df.dropna(subset=["TMAX", "TMIN"], how="all").copy()

    # Fill TAVG with mean of TMAX and TMIN where missing
    df["TAVG"] = df["TAVG"].fillna((df["TMAX"] + df["TMIN"]) / 2)

    # Calculate HDD = max(0, 65 - TAVG)
    df["HDD"] = (65 - df["TAVG"]).clip(lower=0)

    # Convert to datetime and extract month
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["month"] = df["DATE"].dt.to_period("M")

    # Average HDD across stations for each day, then sum monthly
    daily_avg_hdd = df.groupby("DATE")["HDD"].mean().reset_index()
    daily_avg_hdd["month"] = daily_avg_hdd["DATE"].dt.to_period("M")
    monthly_hdd = daily_avg_hdd.groupby("month")["HDD"].sum().reset_index()

    # Format month
    monthly_hdd["month"] = monthly_hdd["month"].astype(str)
    monthly_hdd["HDD"] = monthly_hdd["HDD"].round(0).astype(int)

    return monthly_hdd

# -----------------------------------
# Process EIA Gas Demand Data
# -----------------------------------

def process_eia(filepath):
    df = pd.read_csv(filepath, skiprows=2)

    # Rename columns
    df = df.rename(columns={
        "Date": "month",
        "Natural Gas Delivered to Consumers in the District of Columbia (Including Vehicle Fuel) (MMcf)": "gas_demand"
    })

    # Drop missing values
    df = df.dropna(subset=["month", "gas_demand"])

    # Format and convert
    df["month"] = pd.to_datetime(df["month"]).dt.to_period("M").astype(str)
    df["gas_demand"] = df["gas_demand"].astype(int)

    return df

# -----------------------------------
# Merge and Save
# -----------------------------------

def main():
    noaa_df = process_noaa(noaa_path)
    eia_df = process_eia(eia_path)

    # Inner join on month to keep only overlapping periods
    merged = pd.merge(noaa_df, eia_df, on="month", how="inner").sort_values("month")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save final dataset
    merged.to_csv(output_path, index=False)
    print(f"✅ modeling_dataset.csv created at: {output_path}")

if __name__ == "__main__":
    main()
