# This file will contain the model that I use to predict future outcomes (forecasted energy demand)


import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def get_models():
    """Returns a list of (model, name) tuples."""
    return [
        (LinearRegression(), "Linear Regression"),
        (Ridge(alpha=1.0), "Ridge Regression"),
        (Lasso(alpha=0.1), "Lasso Regression"),
        (RandomForestRegressor(n_estimators=100, random_state=42), "Random Forest"),
        (XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), "XGBoost")
    ]

def train_and_evaluate(model, model_name, df, feature_cols, target_col):
    """Train the given model and return evaluation metrics and predictions."""
    X = df[feature_cols]
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    return {
        "model": model_name,
        "r2_score": round(r2, 4),
        "mae": round(mae, 2),
        "y_test": y_test,
        "y_pred": y_pred
    }


