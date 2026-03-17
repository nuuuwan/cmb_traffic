import os
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from cmb_traffic.readme.ReadMeIndexChartUtilsMixin import \
    ReadMeIndexChartUtilsMixin
from utils_future import TimeUtils

log = Log("ReadMe")


class ReadMeIndexChartSpeedByDayOfWeekMixin(ReadMeIndexChartUtilsMixin):
    def build_speed_by_day_of_week_chart(self, journey_d_list):
        plt.close()
        journey_d_list = self.filter_to_chart_days(journey_d_list)
        if not journey_d_list or len(journey_d_list) < 30:
            return None

        ut_starts = [d["ut_start"] for d in journey_d_list]
        min_ut_start = min(ut_starts)
        max_ut_start = max(ut_starts)

        min_dt = datetime.fromtimestamp(min_ut_start, tz=TimeUtils.LK_TZ)
        max_dt = datetime.fromtimestamp(max_ut_start, tz=TimeUtils.LK_TZ)

        end_of_first_day = datetime(
            min_dt.year,
            min_dt.month,
            min_dt.day,
            23,
            59,
            59,
            999999,
            tzinfo=TimeUtils.LK_TZ,
        )
        display_min_ut_start = int(end_of_first_day.timestamp())

        start_of_last_day = datetime(
            max_dt.year,
            max_dt.month,
            max_dt.day,
            0,
            0,
            0,
            0,
            tzinfo=TimeUtils.LK_TZ,
        )
        display_max_ut_start = int(start_of_last_day.timestamp())

        dow_to_speeds = defaultdict(list)
        for d in journey_d_list:
            if d["ut_start"] < display_min_ut_start:
                continue
            if d["ut_start"] > display_max_ut_start:
                continue
            dt = datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
            dow = dt.weekday()
            dow_to_speeds[dow].append(d["direct_speed_kmph"])
        days = sorted(dow_to_speeds.keys())

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_labels = [day_names[d] for d in days]
        speed_data = [dow_to_speeds[d] for d in days]

        plt.figure(figsize=(8, 4.5))

        bp = plt.boxplot(
            speed_data,
            positions=days,
            widths=0.6,
            patch_artist=True,
            showfliers=True,
        )

        for patch in bp["boxes"]:
            patch.set_facecolor("lightgreen")
            patch.set_alpha(0.7)

        for median in bp["medians"]:
            median.set_color("orange")
            median.set_linewidth(2)

        period_label = self.get_period_label(journey_d_list)
        plt.xlabel("Day of Week")
        plt.ylabel("Speed (km/h)")
        plt.title(
            f"{self.title} - Speed Distribution by Day of Week"
            f"\n{period_label}"
        )
        plt.xticks(days, day_labels)
        plt.grid(True, alpha=0.3, axis="y")

        explanation = (
            "Box: 25th-75th percentile | "
            "Orange line: Median | "
            "Whiskers: Data range | "
            "Dots: Outliers"
        )
        plt.figtext(
            0.5,
            0.0,
            explanation,
            ha="center",
            fontsize=8,
            style="italic",
            color="gray",
        )

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, f"{self.id}.speed_by_day_of_week.png"
        )
        plt.tight_layout()
        plt.savefig(chart_path, dpi=150)
        plt.close()
        log.info(f"Wrote chart to {chart_path}")
        return chart_path
