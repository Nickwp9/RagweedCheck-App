from datetime import datetime, timezone
from ragweed.providers.replay import ReplayProvider


def test_replay_reads_csv(tmp_path):
    f = tmp_path / "sample.csv"
    f.write_text(
        "latitude,longitude,elevation,utc_offset_seconds,timezone,timezone_abbreviation\n"
        "47.0,28.900002,52.0,0,GMT,GMT\n"
        "\n"
        "time,ragweed_pollen (grains/m³)\n"
        "2026-10-13T18:00,0.0\n"
        "\n"
        "time,ragweed_pollen (grains/m³)\n"
        "2026-08-20T00:00,0.0\n"
        "2026-08-20T01:00,5.5\n"
        "2026-08-20T02:00,NaN\n"
        "2026-08-20T03:00,30.0\n",
        encoding="utf-8",
    )
    start = datetime(2026, 8, 20, tzinfo=timezone.utc)
    points = ReplayProvider(f, start=start).fetch(47.0, 28.9, days=1)
    assert len(points) == 4
    assert points[0].time == start
    assert points[1].value == 5.5
    assert points[2].value is None