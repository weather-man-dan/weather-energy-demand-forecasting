# This file will contain the python code to import relevant data sets (NOAA, EIA Data, etc)


import pandas as pd

def load_noaa_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df

def load_eia_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df
