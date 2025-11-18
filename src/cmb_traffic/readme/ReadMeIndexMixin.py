import os
from collections import defaultdict
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from utils import Log

from utils_future import PlotUtils, TimeUtils

log = Log("ReadMe")


class ReadMeIndexMixin:
    @staticmethod
    def append_ttrs(journey_d_list):
        updated_journey_d_list = []
        max_direct_speed_kmph = max(
            [d["direct_speed_kmph"] for d in journey_d_list]
        )

        for d in journey_d_list:
            direct_speed_kmph = d["direct_speed_kmph"]
            d["ttr"] = max_direct_speed_kmph / direct_speed_kmph
            updated_journey_d_list.append(d)

        return updated_journey_d_list

    def build_ttr_chart(self, journey_d_list):
        journey_d_list = self.append_ttrs(journey_d_list)
        start_times = [
            datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
            for d in journey_d_list
        ]
        ttr_values = [d["ttr"] for d in journey_d_list]
        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, ttr_values, label="TTR", color="red")

        current_ttr_value = ttr_values[-1]

        for [ttr, color] in [
            [min(ttr_values), "green"],
            [max(ttr_values), "red"],
        ]:
            ttr_time = start_times[ttr_values.index(ttr)]
            plt.annotate(
                f"{ttr:.2f}x"
                + f" @ {ttr_time.strftime(PlotUtils.TIME_FORMAT_LONG)}",
                xy=(ttr_time, ttr),
                xytext=(5, 0),
                textcoords="offset points",
                fontsize=9,
                color=color,
            )

        plt.xlabel("Start Time")
        plt.ylabel("Travel Time Ratio (TTR)")
        plt.title("Colombo Traffic Index (CTI) as Travel Time Ratio (TTR)")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_ttr_traffic_index.png"
        )
        return PlotUtils.write(chart_path), current_ttr_value

    def build_direct_speed_chart(self, journey_d_list):
        start_times = [
            datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
            for d in journey_d_list
        ]
        direct_speed_kmphs = [d["direct_speed_kmph"] for d in journey_d_list]

        plt.figure(figsize=(8, 4.5))
        plt.plot(
            start_times,
            direct_speed_kmphs,
            label="Direct Speed",
            color="green",
        )

        for [speed, color] in [
            [min(direct_speed_kmphs), "red"],
            [max(direct_speed_kmphs), "green"],
        ]:
            speed_time = start_times[direct_speed_kmphs.index(speed)]
            plt.annotate(
                f"{speed:.1f} km/h"
                + f" @ {speed_time.strftime(PlotUtils.TIME_FORMAT_LONG)}",
                xy=(speed_time, speed),
                xytext=(5, 0),
                textcoords="offset points",
                fontsize=9,
                color=color,
            )

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=TimeUtils.LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Start Time")
        plt.ylabel("Overall Direct Speed (km/h)")
        plt.title("Overall Direct Speed (km/h)")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_overall_traffic_index.png"
        )
        return PlotUtils.write(chart_path)

    def build_ttr_by_time_of_day_chart(self, journey_d_list):

        if not journey_d_list:
            return None

        journey_d_list = self.append_ttrs(journey_d_list)

        hour_to_ttrs = defaultdict(list)
        for d in journey_d_list:
            dt = datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
            hour = dt.hour
            hour_to_ttrs[hour].append(d["ttr"])

        hours = sorted(hour_to_ttrs.keys())
        avg_ttrs = [sum(hour_to_ttrs[h]) / len(hour_to_ttrs[h]) for h in hours]

        plt.figure(figsize=(8, 4.5))
        plt.plot(
            hours,
            avg_ttrs,
            label="Average TTR by Hour",
            color="red",
            linewidth=3,
        )

        for [ttr, color] in [
            [min(avg_ttrs), "green"],
            [max(avg_ttrs), "red"],
        ]:
            hour = hours[avg_ttrs.index(ttr)]
            hour_str = datetime(2000, 1, 1, hour).strftime(
                PlotUtils.TIME_ONLY_FORMAT
            )
            plt.annotate(
                f"{ttr:.2f}x @ {hour_str}",
                xy=(hour, ttr),
                xytext=(5, 0),
                textcoords="offset points",
                fontsize=9,
                color=color,
            )

        plt.xlabel("Hour of Day")
        plt.ylabel("Average Travel Time Ratio (TTR)")
        plt.title("Average CTI by Time of Day")

        hour_labels = [
            datetime(2000, 1, 1, h).strftime(PlotUtils.TIME_ONLY_FORMAT)
            for h in range(0, 24, 4)
        ]
        plt.xticks(range(0, 24, 4), hour_labels)
        plt.grid(True, alpha=0.3)

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_ttr_by_time_of_day.png"
        )
        plt.tight_layout()
        plt.savefig(chart_path, dpi=150)
        plt.close()
        log.info(f"Wrote chart to {chart_path}")
        return chart_path

    def build_speed_by_day_of_week_chart(self, journey_d_list):
        if not journey_d_list:
            return None

        dow_to_speeds = defaultdict(list)
        for d in journey_d_list:
            dt = datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
            dow = dt.weekday()
            dow_to_speeds[dow].append(d["direct_speed_kmph"])
        days = sorted(dow_to_speeds.keys())

        p10_speeds = [np.percentile(dow_to_speeds[d], 10) for d in days]
        median_speeds = [np.percentile(dow_to_speeds[d], 50) for d in days]
        p90_speeds = [np.percentile(dow_to_speeds[d], 90) for d in days]

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_labels = [day_names[d] for d in days]

        plt.figure(figsize=(8, 4.5))

        plt.plot(
            days,
            p10_speeds,
            label="10th Percentile",
            color="red",
            linewidth=2,
            marker="o",
        )
        plt.plot(
            days,
            median_speeds,
            label="Median",
            color="orange",
            linewidth=3,
            marker="o",
        )
        plt.plot(
            days,
            p90_speeds,
            label="90th Percentile",
            color="green",
            linewidth=2,
            marker="o",
        )

        plt.xlabel("Day of Week")
        plt.ylabel("Speed (km/h)")
        plt.title("Speed by Day of Week (P10/Median/P90)")
        plt.xticks(days, day_labels)
        plt.legend()
        plt.grid(True, alpha=0.3)

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_speed_by_day_of_week.png"
        )
        plt.tight_layout()
        plt.savefig(chart_path, dpi=150)
        plt.close()
        log.info(f"Wrote chart to {chart_path}")
        return chart_path

    def get_lines_for_cti(self, journey_d_list) -> list[str]:
        lines = []

        ttr_chart_path, current_ttr_value = self.build_ttr_chart(
            journey_d_list
        )
        lines.extend(
            [
                f"## Colombo Traffic Index (CTI) = {current_ttr_value:.2f}x",
                "",
            ]
        )

        lines.extend([f"![{ttr_chart_path}]({ttr_chart_path})", ""])

        lines.extend(["### Average CTI by Time of Day", ""])
        ttr_by_hour_path = self.build_ttr_by_time_of_day_chart(journey_d_list)
        if ttr_by_hour_path:
            lines.extend([f"![{ttr_by_hour_path}]({ttr_by_hour_path})", ""])

        lines.extend(["### Average Speed by Day of Week", ""])
        speed_by_dow_path = self.build_speed_by_day_of_week_chart(
            journey_d_list
        )
        if speed_by_dow_path:
            lines.extend([f"![{speed_by_dow_path}]({speed_by_dow_path})", ""])

        lines.extend(["### Overall Direct Speed (ODS)", ""])
        chart_path = self.build_direct_speed_chart(journey_d_list)
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines
