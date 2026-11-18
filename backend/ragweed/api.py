from datetime import datetime, timezone, date
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from ragweed.alerts import find_high_windows, daily_means, level_for
from ragweed.providers.replay import ReplayProvider
from ragweed.settings import REPLAY_NOW, FORECAST_DAYS, DEFAULT_MIN_HOURS

DATA = Path(__file__).parent.parent / "data" / "ragweed_2026_chisinau.csv"

app = FastAPI(title="Ragweed Alert API")


class PointOut(BaseModel):
    time: datetime
    value: float | None


class WindowOut(BaseModel):
    start: datetime
    end: datetime
    hours: int
    peak: float


class DayOut(BaseModel):
    day: date
    mean: float
    level: str


class ForecastOut(BaseModel):
    fetched_at: datetime
    points: list[PointOut]
    windows: list[WindowOut]
    days: list[DayOut]


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/forecast", response_model=ForecastOut)
def forecast(lat: float = 47.0, lon: float = 28.9, threshold: float = 100, min_hours: int = DEFAULT_MIN_HOURS):
    points = ReplayProvider(DATA, REPLAY_NOW).fetch(lat, lon, FORECAST_DAYS)
    windows = find_high_windows(points, threshold, min_hours)
    return ForecastOut(
        fetched_at=REPLAY_NOW,
        points=[PointOut(time=p.time, value=p.value) for p in points],
        windows=[WindowOut(start=w.start, end=w.end, hours=w.hours, peak=w.peak) for w in windows],
        days=[DayOut(day=d, mean=round(m, 1), level=level_for(m)) for d, m in daily_means(points).items()],
    )