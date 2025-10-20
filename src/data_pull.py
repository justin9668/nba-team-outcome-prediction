#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder

def pull_season(season: str, season_type: str) -> pd.DataFrame:
    # season like "2023-24", season_type like "Regular Season"
    lgf = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable=season_type
    )
    df = lgf.get_data_frames()[0]
    # ensure consistent types
    df["GAME_ID"] = df["GAME_ID"].astype(str)
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", required=True, help='e.g. "2023-24"')
    ap.add_argument("--season_type", default="Regular Season")
    ap.add_argument("--out", default="data/raw/team_gamelogs.csv")
    args = ap.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df = pull_season(args.season, args.season_type)
    df.to_csv(args.out, index=False)
    print(f"[OK] wrote {args.out} rows={len(df):,} games={df['GAME_ID'].nunique():,}")

if __name__ == "__main__":
    main()
