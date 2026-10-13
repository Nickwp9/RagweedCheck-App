from datetime import datetime, timedelta

from ragweed.alerts import find_high_windows
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