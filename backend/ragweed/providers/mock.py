import math
from datetime import datetime, timedelta
from ragweed.models import HourlyPoint

class MockProvider:

    def fetch(self, lat, lon, days):
        points = []
        start = datetime.now().replace(minute=0, second=0, microsecond=0)
        for i in range(24 * days):
            t = start + timedelta(hours=i)
            hour = t.hour
            if hour < 6 or hour > 20:
                value = 0.0
            else:
                fraction = (hour - 6) / (20 - 6)
                value = 80 * math.sin(fraction * math.pi)
            points.append(HourlyPoint(t, value))
        return points