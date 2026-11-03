from datetime import datetime
import pandas as pd
from ragweed.models import HourlyPoint

class ReplayProvider:

    def __init__(self, path, start: datetime):
        self.path = path
        self.start = start  # must be timezone-aware (UTC)

    def fetch(self, lat: float, lon: float, days: int) -> list[HourlyPoint]:
        with open(self.path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        # The hourly data follows the last "time,..." header line.
        header = max(i for i, line in enumerate(lines) if line.startswith("time"))

        df = pd.read_csv(
            self.path,
            skiprows=header,
            usecols=[0, 1],
            names=["time", "ragweed"],
            header=0,
            parse_dates=["time"],
            encoding="utf-8",
        )
        df["time"] = df["time"].dt.tz_localize("UTC")
        df = df[df["time"] >= self.start].head(days * 24)

        return [
            HourlyPoint(
                row.time.to_pydatetime(),
                None if pd.isna(row.ragweed) else float(row.ragweed),
            )
            for row in df.itertuples()
        ]