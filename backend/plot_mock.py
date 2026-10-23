import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from ragweed.providers.mock import MockProvider


points = MockProvider().fetch(47.0, 28.8, days=60)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot([p.time for p in points], [p.value for p in points])
ax.axhline(20, color="red", linestyle="--")  # alert threshold

ax.set_xlabel("Time")
ax.set_ylabel("ragweed (grains/m3)")

locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
ax.grid(axis="x", alpha=0.3)

plt.show()