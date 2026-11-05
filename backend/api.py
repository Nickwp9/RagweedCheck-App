from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from ragweed.alerts import find_high_windows
from ragweed.providers.replay import ReplayProvider

DATA = Path(__file__).parent.parent / "data" / "ragweed_2026_chisinau.csv"
REPLAY_NOW = datetime(2026, 8, 25, 6, tzinfo=timezone.utc)

app = FastAPI(title="Ragweed Alert API")


class PointOut(BaseModel):
    time: datetime
    value: float | None


class WindowOut(BaseModel):
    start: datetime
    end: datetime
    hours: int
    peak: float


class ForecastOut(BaseModel):
    fetched_at: datetime
    points: list[PointOut]
    windows: list[WindowOut]


@app.get("/forecast", response_model=ForecastOut)
def forecast(lat: float = 47.0, lon: float = 28.9, threshold: float = 100, min_hours: int = 1):
    points = ReplayProvider(DATA, REPLAY_NOW).fetch(lat, lon, 72)
    windows = find_high_windows(points, threshold, min_hours)
    return ForecastOut(
        fetched_at=REPLAY_NOW,
        points=[PointOut(time=p.time, value=p.value) for p in points],
        windows=[
            WindowOut(start=w.start, end=w.end, hours=w.hours, peak=w.peak)
            for w in windows
        ],
    )