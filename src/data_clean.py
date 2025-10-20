#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
from dateutil import parser as dp

def normalize_columns(df):
    df = df.copy()
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace("%","pct", regex=False)
                  .str.replace("-","_", regex=False)
                  .str.replace(" ","_", regex=False))
    return df

def parse_game_date_col(df):
    df = df.copy()
    df["game_date"] = pd.to_datetime(df["game_date"].apply(lambda s: dp.parse(str(s)).date()))
    return df

def add_home_flag(df):
    df = df.copy()
    # Treat missing matchup as not-home (False). 'vs.' = home, '@' = away.
    df["home"] = df["matchup"].str.contains(r"vs\.", regex=True, na=False).astype("int8")
    return df


def add_rest_days(df):
    df = df.sort_values(["team_id","game_date"]).copy()
    df["prev_date"] = df.groupby("team_id")["game_date"].shift(1)
    df["rest_days"] = (df["game_date"] - df["prev_date"]).dt.days.fillna(3)
    return df.drop(columns=["prev_date"])

def attach_opponent(df):
    df = df.copy()
    opp = df[["game_id","team_id","team_abbreviation","pts","fg_pct","reb","tov"]].rename(columns={
        "team_id":"opponent_team_id",
        "team_abbreviation":"opponent_team_abbreviation",
        "pts":"opponent_pts",
        "fg_pct":"opponent_fg_pct",
        "reb":"opponent_reb",
        "tov":"opponent_tov",
    })
    m = pd.merge(df, opp, on="game_id", how="left")
    return m[m["opponent_team_id"] != m["team_id"]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", default="data/raw/team_gamelogs.csv")
    ap.add_argument("--outfile", default="data/processed/team_games_clean.csv")
    args = ap.parse_args()

    Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.infile, dtype={"GAME_ID": str})
    df = normalize_columns(df)
    df = parse_game_date_col(df)
    df = add_home_flag(df)
    df = add_rest_days(df)
    df = attach_opponent(df)
    
    # keep only games that have exactly 2 team rows
    pair_counts = df.groupby("game_id")["team_id"].transform("nunique")
    df = df[pair_counts == 2].copy()

    keep = [c for c in [
        "season_id","team_id","team_abbreviation","team_name","game_id","game_date","matchup","wl",
        "pts","fg_pct","fga","fgm","fg3m","fg3a","fg3_pct","ftm","fta","ft_pct","oreb","dreb","reb",
        "ast","stl","blk","tov","pf","plus_minus","home","rest_days",
        "opponent_team_id","opponent_team_abbreviation","opponent_pts","opponent_fg_pct","opponent_reb","opponent_tov"
    ] if c in df.columns]

    out = (df.drop_duplicates(subset=["team_id","game_id"])
             .sort_values(["game_date","game_id","team_id"])[keep])

    out.to_csv(args.outfile, index=False)
    print(f"[OK] wrote {args.outfile} rows={len(out):,} uniq_games={out['game_id'].nunique():,}")

if __name__ == "__main__":
    main()
