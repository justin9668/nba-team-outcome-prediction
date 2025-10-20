import pandas as pd

df = pd.read_csv("data/processed/team_games_clean.csv", parse_dates=["game_date"])
assert df["game_id"].nunique() * 2 == len(df), "Each game must have 2 rows"
assert {"pts","fg_pct","reb","tov","opponent_pts"}.issubset(df.columns), "Missing key columns"
print("✅ verified:", df.shape, "games:", df["game_id"].nunique(),
      "range:", df["game_date"].min(), "→", df["game_date"].max())
