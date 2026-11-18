"""A pitcher's arsenal, what he throws in each count, and how his velocity holds up, with FastballAPI.

    pip install -r requirements.txt
    export FASTBALLAPI_API_KEY=...     # free key: https://fastballapi.com/signup

    python pitch_mix.py "Tarik Skubal" --season 2025
    python pitch_mix.py "Paul Skenes" --season 2025 --csv skenes_2025.csv

Credits: search 1, the arsenal 5, every pitch of a season 10 per 2,000 pitches
(about 20 for a starter's season). All of it fits in the free 500 credits a month.
"""
import argparse

import pandas as pd
from fastballapi import Client

FASTBALLS = {"FF", "SI", "FT", "FC"}


def count_state(balls, strikes):
    if balls == 0 and strikes == 0:
        return "first pitch"
    if strikes == 2:
        return "two strikes"
    if strikes > balls:
        return "ahead"
    if balls > strikes:
        return "behind"
    return "even"


def season_pitches(client, pitcher_id, season):
    rows, offset = [], 0
    while offset is not None:
        # client.call reaches any tool by name, so this works on every client version.
        page = client.call("get_pitches", {"pitcher_id": pitcher_id, "season": season, "limit": 2000, "offset": offset})
        rows += page["pitches"]
        offset = page.get("next_offset") if len(page["pitches"]) == 2000 else None
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--season", type=int, default=2025)
    ap.add_argument("--csv", help="also write every pitch to this file")
    args = ap.parse_args()

    client = Client()
    found = client.search_players(args.name, limit=1)["players"]
    if not found:
        raise SystemExit(f"No player found for {args.name!r}")
    pitcher = found[0]

    mix = client.call("get_pitch_mix", {"pitcher_id": pitcher["player_id"], "season": args.season})
    print(f"{pitcher['name']} {args.season}: {mix['pitches']:,} pitches")
    print(pd.DataFrame(mix["mix"])[["name", "usage", "avg_velocity", "max_velocity", "whiff_rate", "ball_rate"]].to_string(index=False))

    df = season_pitches(client, pitcher["player_id"], args.season)
    df = df[df["pitch_type"].notna()]
    df["count"] = [count_state(b, s) for b, s in zip(df["balls"], df["strikes"])]

    print("\nWhat he throws by count (share of pitches):")
    by_count = pd.crosstab(df["pitch_type_name"], df["count"], normalize="columns")
    cols = [c for c in ["first pitch", "ahead", "even", "behind", "two strikes"] if c in by_count.columns]
    print((by_count[cols] * 100).round(1).to_string())

    fb = df[df["pitch_type"].isin(FASTBALLS) & df["velocity"].notna()]
    if len(fb):
        main_fb = fb["pitch_type_name"].value_counts().index[0]
        velo = fb[fb["pitch_type_name"] == main_fb].groupby("inning")["velocity"].agg(["mean", "count"])
        velo = velo[velo["count"] >= 20]
        print(f"\n{main_fb} velocity by inning (innings with 20+ of them):")
        print(velo.round(1).rename(columns={"mean": "avg mph", "count": "pitches"}).to_string())

    if args.csv:
        df.to_csv(args.csv, index=False)
        print(f"\n{len(df):,} pitches written to {args.csv}")
    print("credits left:", client.last_credits_remaining)


if __name__ == "__main__":
    main()
