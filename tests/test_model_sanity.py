import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

CLEAN_DATA_PATH = Path("data/processed/team_games_clean.csv")
MODEL_PATH = Path("models/final_linear_regression.joblib")

CANDIDATE_FEATURES = [
    "home", "rest_days", "fg_pct", "fga", "fgm",
    "reb", "ast", "tov",
    "opponent_pts", "opponent_fg_pct", "opponent_reb", "opponent_tov"
]

def test_model_file_exists():
    """Verify trained model file exists."""
    assert MODEL_PATH.exists(), f"Model not found at {MODEL_PATH}"

def test_can_train_model():
    """Verify we can train a model on a subset of data."""
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["game_date"])
    
    # Use first 100 rows for quick test
    df_subset = df.head(100)
    
    X = df_subset[CANDIDATE_FEATURES].dropna()
    y = df_subset.loc[X.index, "pts"]
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Verify model has coefficients
    assert len(model.coef_) == len(CANDIDATE_FEATURES)
    assert model.coef_ is not None

def test_predictions_are_reasonable():
    """Verify predictions are in reasonable range."""
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["game_date"])
    
    df_subset = df.head(100)
    X = df_subset[CANDIDATE_FEATURES].dropna()
    y = df_subset.loc[X.index, "pts"]
    
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)
    
    # NBA team scores typically 80-150 points
    assert (predictions >= 70).all(), "Predictions too low"
    assert (predictions <= 160).all(), "Predictions too high"

def test_baseline_improvement():
    """Verify model beats baseline on subset."""
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["game_date"])
    
    # Chronological split on subset
    df_subset = df.head(200).sort_values("game_date")
    split_idx = int(len(df_subset) * 0.8)
    
    train_df = df_subset.iloc[:split_idx]
    test_df = df_subset.iloc[split_idx:]
    
    # Train model
    X_train = train_df[CANDIDATE_FEATURES].dropna()
    y_train = train_df.loc[X_train.index, "pts"]
    
    X_test = test_df[CANDIDATE_FEATURES].dropna()
    y_test = test_df.loc[X_test.index, "pts"]
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    # Baseline: team average
    team_avg = train_df.groupby("team_abbreviation")["pts"].mean().to_dict()
    test_with_baseline = test_df.loc[y_test.index].copy()
    test_with_baseline["baseline_pred"] = test_with_baseline["team_abbreviation"].map(team_avg)
    
    model_mae = mean_absolute_error(y_test, predictions)
    baseline_mae = mean_absolute_error(y_test, test_with_baseline["baseline_pred"])
    
    # Model should beat baseline
    assert model_mae < baseline_mae, f"Model MAE ({model_mae:.2f}) not better than baseline ({baseline_mae:.2f})"