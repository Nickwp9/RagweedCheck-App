import argparse
from datetime import datetime, timezone
from ragweed.alerts import find_high_windows
from ragweed.providers.mock import MockProvider
from ragweed.providers.replay import ReplayProvider

def main():
    parser = argparse.ArgumentParser(description="Ragweed alert checker")
    parser.add_argument("--threshold", type=float, default=20,
                        help="grains/m3 considered high")
    parser.add_argument("--min-hours", type=int, default=3,
                        help="hours the level must stay above the threshold")
    parser.add_argument("--days", type=int, default=3,
                        help="forecast length in days")
    parser.add_argument("--replay", default=None,
                        help="path to a saved CSV to replay")
    parser.add_argument("--start", default=None,
                        help="replay start date, e.g. 2026-08-25")
    args = parser.parse_args()

    if args.replay:
        if not args.start:
            parser.error("--replay needs --start")
        start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
        provider = ReplayProvider(args.replay, start)
    else:
        provider = MockProvider()

    points = provider.fetch(47.0, 28.8, args.days)
    if not points:
        print("No data from that start date.")
        return

    windows = find_high_windows(points, args.threshold, args.min_hours)
    if not windows:
        print("No high-ragweed windows in this forecast.")
        return

    for w in windows:
        print(f"{w.start:%a %d %b %H:%M} -> {w.end:%a %d %b %H:%M} "
              f"({w.hours} h, peak {w.peak:.1f})")


if __name__ == "__main__":
    main()