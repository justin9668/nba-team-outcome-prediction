import pytest
import pandas as pd
from pathlib import Path

# Paths relative to project root
RAW_DATA_PATH = Path("data/raw/team_gamelogs.csv")
CLEAN_DATA_PATH = Path("data/processed/team_games_clean.csv")

def test_raw_data_exists():
    """Verify raw data file exists."""
    assert RAW_DATA_PATH.exists(), f"Raw data not found at {RAW_DATA_PATH}"

def test_clean_data_exists():
    """Verify cleaned data file exists."""
    assert CLEAN_DATA_PATH.exists(), f"Clean data not found at {CLEAN_DATA_PATH}"

def test_clean_data_structure():
    """Verify cleaned data has expected structure."""
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["game_date"])
    
    # Check required columns exist
    required_cols = {
        "game_id", "team_abbreviation", "pts", "home", "rest_days",
        "fg_pct", "reb", "tov", "opponent_pts", "opponent_fg_pct", 
        "opponent_reb", "opponent_tov"
    }
    assert required_cols.issubset(df.columns), f"Missing required columns"

def test_games_appear_twice():
    """Verify each game has exactly 2 team rows."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    game_counts = df.groupby("game_id").size()
    
    assert (game_counts == 2).all(), "Some games don't have exactly 2 rows"

def test_no_missing_critical_values():
    """Verify no missing values in critical columns."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    critical_cols = ["pts", "team_abbreviation", "game_id", "home"]
    
    for col in critical_cols:
        assert df[col].notna().all(), f"Missing values found in {col}"

def test_date_range():
    """Verify data covers expected season."""
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["game_date"])
    
    min_date = df["game_date"].min()
    max_date = df["game_date"].max()
    
    # 2023-24 season roughly Oct 2023 to April 2024
    assert min_date.year == 2023 and min_date.month >= 10
    assert max_date.year == 2024 and max_date.month <= 4

def test_valid_team_abbreviations():
    """Verify only valid NBA teams are present."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    NBA_TEAMS = {
        "ATL","BOS","BKN","CHA","CHI","CLE","DAL","DEN",
        "DET","GSW","HOU","IND","LAC","LAL","MEM","MIA",
        "MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHX",
        "POR","SAC","SAS","TOR","UTA","WAS"
    }
    
    actual_teams = set(df["team_abbreviation"].unique())
    assert actual_teams.issubset(NBA_TEAMS), f"Invalid teams found: {actual_teams - NBA_TEAMS}"


def test_win_loss_consistency():
    """Verify W/L flags are opposite for same game."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    # Sample 100 games for efficiency
    for game_id in df["game_id"].unique()[:100]:
        game = df[df["game_id"] == game_id]
        wl_values = set(game["wl"].unique())
        assert wl_values == {"W", "L"}, f"Game {game_id} doesn't have exactly one W and one L"


def test_plus_minus_symmetry():
    """Verify plus_minus values sum to approximately 0 for most games."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    plus_minus_sum = df.groupby("game_id")["plus_minus"].sum()
    
    # Allow for some games with small discrepancies (overtime, data recording)
    # Most games should sum to 0 within tolerance
    close_to_zero = (plus_minus_sum.abs() < 2.5).sum()
    total_games = len(plus_minus_sum)
    
    assert close_to_zero / total_games > 0.95, f"Only {close_to_zero}/{total_games} games have plus_minus near 0"


def test_points_consistency():
    """Verify team's points match opponent's opponent_pts."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    # Sample 100 games for efficiency
    for game_id in df["game_id"].unique()[:100]:
        game = df[df["game_id"] == game_id].sort_values("team_id")
        
        team1_pts = game.iloc[0]["pts"]
        team2_opp_pts = game.iloc[1]["opponent_pts"]
        team2_pts = game.iloc[1]["pts"]
        team1_opp_pts = game.iloc[0]["opponent_pts"]
        
        assert team1_pts == team2_opp_pts, f"Points mismatch in game {game_id}"
        assert team2_pts == team1_opp_pts, f"Points mismatch in game {game_id}"


def test_home_away_balance():
    """Verify each game has exactly one home and one away team."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    home_per_game = df.groupby("game_id")["home"].sum()
    
    assert (home_per_game == 1).all(), "Each game should have exactly 1 home team"


def test_percentage_ranges():
    """Verify shooting percentages are between 0 and 1."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    pct_cols = ["fg_pct", "fg3_pct", "ft_pct", "opponent_fg_pct"]
    
    for col in pct_cols:
        valid_values = df[col].dropna()
        assert (valid_values >= 0).all(), f"{col} has values below 0"
        assert (valid_values <= 1).all(), f"{col} has values above 1"


def test_rest_days_reasonable():
    """Verify rest days are reasonable (0-20 days)."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    assert (df["rest_days"] >= 0).all(), "Negative rest days found"
    assert (df["rest_days"] <= 20).all(), "Unreasonably long rest periods found"


def test_home_court_advantage():
    """Verify home teams score more on average (expected NBA pattern)."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    home_pts = df[df["home"] == 1]["pts"].mean()
    away_pts = df[df["home"] == 0]["pts"].mean()
    
    assert home_pts > away_pts, f"Home court advantage not observed: home={home_pts:.2f}, away={away_pts:.2f}"


def test_realistic_score_distribution():
    """Verify team scores follow expected NBA distribution."""
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    mean_pts = df["pts"].mean()
    std_pts = df["pts"].std()
    
    # NBA teams typically average 105-120 points
    assert 100 < mean_pts < 125, f"Mean points {mean_pts:.2f} unrealistic for NBA"
    assert 5 < std_pts < 20, f"Std dev {std_pts:.2f} unrealistic for NBA"