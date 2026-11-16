from datetime import date, datetime, timedelta, timezone
from ragweed.alerts import daily_means, find_high_windows, level_for
from ragweed.models import HourlyPoint


def make_points(values):
    start = datetime(2026, 8, 20, 0, 0)
    return [HourlyPoint(start + timedelta(hours=i), v) for i, v in enumerate(values)]


def test_finds_single_window():
    points = make_points([0, 5, 25, 30, 40, 10, 0])
    windows = find_high_windows(points, threshold=20, min_hours=3)
    assert len(windows) == 1
    assert windows[0].hours == 3
    assert windows[0].peak == 40


def test_level_for():
    assert level_for(5) == "low"
    assert level_for(10) == "moderate"
    assert level_for(49.9) == "moderate"
    assert level_for(50) == "high"
    assert level_for(500) == "very high"


def test_ignores_run_shorter_than_min_hours():
    # first run is only 2 hours (25, 30), second run is 3 hours (40, 40, 40)
    points = make_points([0, 25, 30, 0, 40, 40, 40, 0])
    windows = find_high_windows(points, threshold=20, min_hours=3)
    assert len(windows) == 1
    assert windows[0].peak == 40


def test_none_splits_a_run():
    # 3 high hours, a gap with no data, then 3 more high hours
    points = make_points([30, 30, 30, None, 30, 30, 30])
    windows = find_high_windows(points, threshold=20, min_hours=3)
    assert len(windows) == 2


def test_daily_means_use_local_day():
    pts = [HourlyPoint(datetime(2026, 8, 25, h, tzinfo=timezone.utc), v)
           for h, v in [(12, 50.0), (21, 10.0), (22, 30.0), (23, None)]]
    assert daily_means(pts) == {date(2026, 8, 25): 50.0, date(2026, 8, 26): 20.0}