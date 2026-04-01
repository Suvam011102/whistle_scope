from pathlib import Path

import numpy as np
import pandas as pd


def load_data():
    df = pd.read_csv(Path("data/processed/epl_master.csv")).copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["TotalCards"] = df["HY"] + df["AY"]
    df["TotalFouls"] = df["HF"] + df["AF"]
    df["TotalGoals"] = df["FTHG"] + df["FTAG"]
    df["GoalDiff"] = df["FTHG"] - df["FTAG"]
    df["HomeBias"] = df["AF"] - df["HF"]
    df["CardsPerFoul"] = np.where(df["TotalFouls"] > 0, df["TotalCards"] / df["TotalFouls"], 0)
    df["SeasonStart"] = df["Season"].str[:4].astype(int)
    df["VAR_Era"] = np.where(df["SeasonStart"] >= 2019, "Post-VAR", "Pre-VAR")
    df["Result"] = np.select(
        [df["FTHG"] > df["FTAG"], df["FTHG"] < df["FTAG"]],
        ["Home win", "Away win"],
        default="Draw",
    )

    return df.sort_values(["Date", "HomeTeam"], na_position="last").reset_index(drop=True)
