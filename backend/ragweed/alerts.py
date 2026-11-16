from datetime import date
from zoneinfo import ZoneInfo
from ragweed.models import HourlyPoint, Window
from ragweed.settings import LEVELS


def daily_means(points: list[HourlyPoint], tz: str = "Europe/Chisinau") -> dict[date, float]:
    zone = ZoneInfo(tz)
    groups = {}
    for p in points:
        if p.value is not None:
            groups.setdefault(p.time.astimezone(zone).date(), []).append(p.value)
    return {d: sum(v) / len(v) for d, v in groups.items()}


def level_for(value: float) -> str:
    return [name for name, start in LEVELS if value >= start][-1]


def find_high_windows(points: list[HourlyPoint], threshold: float, min_hours: int) -> list[Window]:
    windows: list[Window] = []
    run: list[HourlyPoint] = []

    def close_run() -> None:
        if len(run) >= min_hours:
            windows.append(Window(run[0].time, run[-1].time, max(p.value for p in run)))
        run.clear()

    for p in points:
        if p.value is not None and p.value >= threshold:
            run.append(p)
        else:
            close_run()
    close_run()
    return windows