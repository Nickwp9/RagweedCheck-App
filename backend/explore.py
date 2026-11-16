import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
from ragweed.alerts import find_high_windows
from ragweed.providers.replay import ReplayProvider


DATA = Path(__file__).parent / "data" / "ragweed_2026_chisinau.csv"


def load_season(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    # The hourly data follows the last "time,..." header line.
    header = max(i for i, line in enumerate(lines) if line.startswith("time"))
    df = pd.read_csv(
        path,
        skiprows=header,
        usecols=[0, 1],
        names=["time", "ragweed"],
        header=0,
        parse_dates=["time"],
        encoding="utf-8",
    )
    df["time"] = df["time"].dt.tz_localize("UTC")
    return df


df = load_season(DATA)

# Part 1: number of windows for each threshold and minimum duration
start = datetime(2026, 7, 13, tzinfo=timezone.utc)
points = ReplayProvider(DATA, start).fetch(47.0, 28.9, 97)

thresholds = [20, 100, 500, 1000, 2000]
durations = [1, 3]

print("threshold   min 1 h   min 3 h")
for threshold in thresholds:
    row = []
    for min_hours in durations:
        row.append(len(find_high_windows(points, threshold, min_hours)))
    print(f"{threshold:<11} {row[0]:<9} {row[1]}")

# Part 2: first time the level reaches 10, 20 and 50
print()
for level in [10, 20, 50]:
    first = df.loc[df["ragweed"] >= level, "time"].min()
    if pd.isna(first):
        print(f"first >= {level}: never reached")
    else:
        print(f"first >= {level}: {first:%a %d %b %H:%M} UTC")

daily = df.set_index("time")["ragweed"].resample("D").mean()
names = [n for n, _ in LEVELS]
cats = pd.cut(daily, bins=[s for _, s in LEVELS] + [float("inf")], labels=names, right=False)
print(cats.value_counts().reindex(names))
print(f"highest daily mean: {daily.max():.1f} on {daily.idxmax():%d %b}")