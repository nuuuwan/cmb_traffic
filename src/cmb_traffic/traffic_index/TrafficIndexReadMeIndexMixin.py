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
                speeds = [d2["avg_speed_kmph"] for d2 in window]
                min_avg_speed_kmph = min(speeds)
                max_avg_speed_kmph = max(speeds)
                ttr = max_avg_speed_kmph / min_avg_speed_kmph
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
        plt.plot(start_times, ttr_values, marker="o")

        plt.xlabel("Start Time")
        plt.ylabel("Travel Time Ratio (TTR)")
        plt.title("Travel Time Ratio (TTR) Over Time")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_ttr_traffic_index.png"
        )
        return PlotUtils.write(chart_path)

    def build_index_chart(self, journey_d_list):

        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=TimeUtils.LK_TZ)
            for d in journey_d_list
        ]
        avg_speed_kmphs = [d["avg_speed_kmph"] for d in journey_d_list]

        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, avg_speed_kmphs, marker="o")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=TimeUtils.LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Start Time")
        plt.ylabel("Average Speed (km/h)")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_overall_traffic_index.png"
        )
        return PlotUtils.write(chart_path)

    def get_lines_for_index(self, journey_d_list) -> list[str]:
        lines = ["## Overall Traffic Index", ""]
        chart_path = self.build_index_chart(journey_d_list)
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        ttr_chart_path = self.build_ttr_chart(journey_d_list)
        lines.extend([f"![{ttr_chart_path}]({ttr_chart_path})", ""])
        return lines
