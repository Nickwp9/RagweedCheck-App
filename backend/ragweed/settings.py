from datetime import datetime, timezone


SENSITIVITY_PRESETS = {
    "extreme": 100,      # your own example
    "high": None,        # TODO: fill from explore.py
    "moderate": None,    # TODO
    "mild": None,        # TODO
}

# 1 hour: with 3, the first days of the season (short windows) would be dropped.
DEFAULT_MIN_HOURS = 1

# How often a user can choose to be notified, in days.
NOTIFY_EVERY_DAYS_CHOICES = (1, 2, 3)

# Level of ragweed that counts as "the season is starting".
SEASON_START_LEVEL = None  # TODO: from the first-date lines in explore.py

# Color cutoffs, as a ratio of the user's threshold.
YELLOW_FROM = 1.0
RED_FROM = 1.5

# Development only: the "pretend now" for the replay, and the forecast length.
REPLAY_NOW = datetime(2026, 8, 25, 6, tzinfo=timezone.utc)
FORECAST_DAYS = 3