import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import Log

from utils_future import PlotUtils, TimeUtils

log = Log("TrafficIndexReadMeIndexMixin")


class TrafficIndexReadMeIndexMixin:
    @staticmethod
    def append_ttrs(journey_d_list):
        n = len(journey_d_list)
        updated_journey_d_list = []
        for i in range(0, n):
            d = journey_d_list[i]
            window = []
            for j in range(i - 1, -1, -1):
                d2 = journey_d_list[j]
                if d2["start_time"] >= d["start_time"] - 3600 * 24:
                    window.append(d2)
                else:
                    break
            if not window:
                ttr = 1.0
            else:
                speeds = [d2["direct_speed_kmph"] for d2 in window]
                min_direct_speed_kmph = min(speeds)
                max_direct_speed_kmph = max(speeds)
                ttr = max_direct_speed_kmph / min_direct_speed_kmph
            d["ttr"] = ttr
            updated_journey_d_list.append(d)
        return updated_journey_d_list

    def build_ttr_chart(self, journey_d_list):
        journey_d_list = self.append_ttrs(journey_d_list)
        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=TimeUtils.LK_TZ)
            for d in journey_d_list
        ]
        ttr_values = [d["ttr"] for d in journey_d_list]
        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, ttr_values, label="TTR", color="red")

        # Annotate min and max TTR values
        for [ttr, color] in [
            [min(ttr_values), "green"],
            [max(ttr_values), "red"],
        ]:
            ttr_time = start_times[ttr_values.index(ttr)]
            plt.annotate(
                f"{ttr:.2f} ({ttr_time.strftime('%Y-%m-%d %H:%M')})",
                xy=(ttr_time, ttr),
                xytext=(10, 20),
                textcoords="offset points",
                fontsize=9,
                color=color,
                bbox=dict(
                    boxstyle="round,pad=0.3", facecolor="white", alpha=0.8
                ),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
            )

        plt.xlabel("Start Time")
        plt.ylabel("Travel Time Ratio (TTR)")
        plt.title("Travel Time Ratio (TTR)")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_ttr_traffic_index.png"
        )
        return PlotUtils.write(chart_path)

    def build_direct_speed_chart(self, journey_d_list):
        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=TimeUtils.LK_TZ)
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
                f"{speed:.1f} km/h ({speed_time.strftime('%Y-%m-%d %H:%M')})",
                xy=(speed_time, speed),
                xytext=(10, 20),
                textcoords="offset points",
                fontsize=9,
                color=color,
                bbox=dict(
                    boxstyle="round,pad=0.3", facecolor="white", alpha=0.8
                ),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
            )

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=TimeUtils.LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Start Time")
        plt.ylabel("Direct Speed (km/h)")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_overall_traffic_index.png"
        )
        return PlotUtils.write(chart_path)

    def get_lines_for_index(self, journey_d_list) -> list[str]:
        lines = ["## Overall Traffic Index", ""]
        chart_path = self.build_direct_speed_chart(journey_d_list)
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        ttr_chart_path = self.build_ttr_chart(journey_d_list)
        lines.extend([f"![{ttr_chart_path}]({ttr_chart_path})", ""])
        return lines
