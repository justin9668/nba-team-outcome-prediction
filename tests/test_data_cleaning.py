import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_clean import normalize_columns, add_home_flag, add_rest_days


def test_normalize_columns():
    """Test column name normalization."""
    df = pd.DataFrame({
        "FG%": [50], 
        "3P-M": [3], 
        "Player Name": ["Test"],
        "FT%": [0.85]
    })
    result = normalize_columns(df)
    
    # Note: % is replaced with "pct" (not "_pct")
    assert "fgpct" in result.columns
    assert "3p_m" in result.columns
    assert "player_name" in result.columns
    assert "ftpct" in result.columns


def test_home_flag_detection():
    """Test home/away flag logic."""
    df = pd.DataFrame({
        "matchup": ["LAL vs. BOS", "LAL @ BOS", None, "DEN vs. PHX"]
    })
    result = add_home_flag(df)
    
    assert result["home"].tolist() == [1, 0, 0, 1]


def test_home_flag_vs_pattern():
    """Test that 'vs.' correctly identifies home games."""
    df = pd.DataFrame({
        "matchup": ["MIA vs. NYK", "GSW vs. LAL", "BOS vs. DEN"]
    })
    result = add_home_flag(df)
    
    assert (result["home"] == 1).all()


def test_home_flag_away_pattern():
    """Test that '@' correctly identifies away games."""
    df = pd.DataFrame({
        "matchup": ["LAL @ GSW", "NYK @ BOS", "CHI @ MIA"]
    })
    result = add_home_flag(df)
    
    assert (result["home"] == 0).all()


def test_rest_days_calculation():
    """Test rest days calculation between games."""
    df = pd.DataFrame({
        "team_id": [1, 1, 1, 1],
        "game_date": pd.to_datetime([
            "2023-10-24", 
            "2023-10-26", 
            "2023-10-29",
            "2023-10-30"
        ])
    })
    result = add_rest_days(df)
    
    # First game defaults to 3 days rest
    assert result["rest_days"].tolist()[0] == 3
    # Second game: 2 days after first
    assert result["rest_days"].tolist()[1] == 2
    # Third game: 3 days after second
    assert result["rest_days"].tolist()[2] == 3
    # Fourth game: 1 day after third (back-to-back)
    assert result["rest_days"].tolist()[3] == 1


def test_rest_days_multiple_teams():
    """Test rest days calculation with multiple teams."""
    df = pd.DataFrame({
        "team_id": [1, 1, 2, 2],
        "game_date": pd.to_datetime([
            "2023-10-24", 
            "2023-10-26", 
            "2023-10-24",
            "2023-10-27"
        ])
    })
    result = add_rest_days(df)
    
    # Each team's first game should have default rest_days
    team1_games = result[result["team_id"] == 1]
    team2_games = result[result["team_id"] == 2]
    
    assert team1_games.iloc[0]["rest_days"] == 3
    assert team1_games.iloc[1]["rest_days"] == 2
    assert team2_games.iloc[0]["rest_days"] == 3
    assert team2_games.iloc[1]["rest_days"] == 3


def test_rest_days_back_to_back():
    """Test back-to-back games (1 day rest)."""
    df = pd.DataFrame({
        "team_id": [1, 1],
        "game_date": pd.to_datetime(["2023-10-24", "2023-10-25"])
    })
    result = add_rest_days(df)
    
    assert result["rest_days"].tolist()[1] == 1


def test_normalize_columns_preserves_data():
    """Test that normalization doesn't change data values."""
    df = pd.DataFrame({
        "FG%": [0.456, 0.523],
        "Points": [110, 105]
    })
    result = normalize_columns(df)
    
    assert result["fgpct"].tolist() == [0.456, 0.523]
    assert result["points"].tolist() == [110, 105]
