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
                f"{ttr:.2f}x"
                + f" @ {ttr_time.strftime(PlotUtils.TIME_FORMAT)}",
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
                f"{speed:.1f} km/h"
                + f" @ {speed_time.strftime(PlotUtils.TIME_FORMAT)}",
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

    def get_lines_for_cti(self, journey_d_list) -> list[str]:
        lines = []

        lines.extend(
            [
                "## Colombo Traffic Index (CTI)",
                "",
            ]
        )
        ttr_chart_path = self.build_ttr_chart(journey_d_list)
        lines.extend([f"![{ttr_chart_path}]({ttr_chart_path})", ""])

        lines.extend(["### Overall Direct Speed (ODS)", ""])
        chart_path = self.build_direct_speed_chart(journey_d_list)
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines
