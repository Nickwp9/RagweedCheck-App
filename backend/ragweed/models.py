from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HourlyPoint:
    time: datetime
    value: float | None  # grains/m3; None = no data (e.g. outside the season)


@dataclass
class Window:
    start: datetime
    end: datetime  # last hour that is still above the threshold
    peak: float

    @property
    def hours(self) -> int:
        return int((self.end - self.start).total_seconds() // 3600) + 1