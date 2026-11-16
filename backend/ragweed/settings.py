from datetime import datetime, timezone

# Weed pollen categories in grains/m3 (24 h average): (name, lowest value of the category).
# TODO: add the source of this scale for the thesis.
LEVELS = [("low", 0), ("moderate", 10), ("high", 50), ("very high", 500)]

# Alert threshold per allergy severity: the category from which the user is warned.
SENSITIVITY_PRESETS = {"severe": 10, "moderate": 50, "mild": 500}

DEFAULT_MIN_HOURS = 1
NOTIFY_EVERY_DAYS_CHOICES = (1, 2, 3)
SEASON_START_LEVEL = 10
YELLOW_FROM = 1.0
RED_FROM = 1.5
REPLAY_NOW = datetime(2026, 8, 25, 6, tzinfo=timezone.utc)
FORECAST_DAYS = 3
SENSITIVITY_PRESETS = {"severe": 10, "moderate": 50, "mild": 200}
SEASON_START_LEVEL = 10