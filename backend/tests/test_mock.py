from datetime import timedelta

from ragweed.providers.mock import MockProvider


def test_mock_returns_hourly_points():
    points = MockProvider().fetch(47.0, 28.8, days=2)
    assert len(points) == 48
    assert points[1].time - points[0].time == timedelta(hours=1)
    assert max(p.value for p in points) > 0