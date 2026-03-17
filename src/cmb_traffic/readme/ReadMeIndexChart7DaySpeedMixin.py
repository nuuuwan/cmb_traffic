import os
from collections import defaultdict
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from utils import Log

from cmb_traffic.readme.ReadMeIndexChartUtilsMixin import \
    ReadMeIndexChartUtilsMixin
from utils_future import TimeUtils

log = Log("ReadMe")

_DATE_FMT = "%Y-%m-%d"
_WINDOW = 7


def _daily_avg_speeds(journey_d_list):
    day_to_speeds = defaultdict(list)
    for d in journey_d_list:
        dt = datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
        day_to_speeds[dt.strftime(_DATE_FMT)].append(d["direct_speed_kmph"])
    rows = sorted(day_to_speeds.items())
    dates = [
        datetime.strptime(r[0], _DATE_FMT).replace(tzinfo=TimeUtils.LK_TZ)
        for r in rows
    ]
    speeds = [sum(r[1]) / len(r[1]) for r in rows]
    return dates, speeds


def _rolling_avg(speeds, window):
    result = []
    for i in range(len(speeds)):
        chunk = speeds[max(0, i - window + 1): i + 1]
        result.append(sum(chunk) / len(chunk))
    return result


class ReadMeIndexChart7DaySpeedMixin(ReadMeIndexChartUtilsMixin):
    def build_7day_speed_chart(self, journey_d_list):
        plt.close()
        if not journey_d_list:
            return None

        dates, daily_speeds = _daily_avg_speeds(journey_d_list)
        ma_speeds = _rolling_avg(daily_speeds, _WINDOW)
        today = max(dates)
        chart_path = self._render_7day_chart(dates, ma_speeds, today)
        return chart_path

    def _render_7day_chart(self, dates, ma_speeds, today):
        def clipped_shift(offset_days):
            delta = timedelta(days=offset_days)
            shifted = [(d + delta, s) for d, s in zip(dates, ma_speeds)]
            filtered = [(d, s) for d, s in shifted if d <= today]
            if not filtered:
                return [], []
            sd, ss = zip(*filtered)
            return list(sd), list(ss)

        dates_7, speeds_7 = clipped_shift(7)
        dates_14, speeds_14 = clipped_shift(14)

        plt.figure(figsize=(10, 5))

        plt.plot(
            dates,
            ma_speeds,
            label=f"{_WINDOW}-day moving avg",
            color="steelblue",
            linewidth=2,
        )
        if dates_7:
            plt.plot(
                dates_7,
                speeds_7,
                label="7 days ago",
                color="orange",
                linewidth=1.5,
                linestyle="dotted",
            )
        if dates_14:
            plt.plot(
                dates_14,
                speeds_14,
                label="14 days ago",
                color="red",
                linewidth=1.5,
                linestyle="dotted",
            )

        period_label = self.get_period_label_from_datetimes(dates)
        plt.xlabel("Date")
        plt.ylabel("Speed (km/h)")
        plt.title(
            f"{self.title} - {_WINDOW}-Day Moving Avg Speed"
            f"\n{period_label}"
        )
        plt.grid(True, alpha=0.2)
        plt.legend()
        plt.tight_layout()

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, f"{self.id}.7day_speed.png"
        )
        plt.savefig(chart_path, dpi=150)
        plt.close()
        log.info(f"Wrote chart to {chart_path}")
        return chart_path
