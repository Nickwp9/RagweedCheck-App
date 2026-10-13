import math
from datetime import datetime, timedelta
class MockProvider:
    def fetch(self, lat, lon, days):

        start = datetime.now().replace(minute = 0, second = 0, microsecond = 0)
        for i in range(24*days):
            t = start + timedelta(hours = i)
            print(t)

a = MockProvider()
a.fetch(1, 2, 3)