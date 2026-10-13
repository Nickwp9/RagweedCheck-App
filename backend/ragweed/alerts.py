from ragweed.models import HourlyPoint, Window


def find_high_windows(
    points: list[HourlyPoint], threshold: float, min_hours: int
) -> list[Window]:
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