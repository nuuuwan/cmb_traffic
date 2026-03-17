import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from cmb_traffic.readme.ReadMeIndexChartUtilsMixin import \
    ReadMeIndexChartUtilsMixin
from utils_future import PlotUtils, TimeUtils


class ReadMeIndexChartDirectSpeedMixin(ReadMeIndexChartUtilsMixin):
    def build_direct_speed_chart(self, journey_d_list):
        plt.close()
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
        plt.title(f"{self.title} - Overall Direct Speed (km/h)")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, f"{self.id}.overall_traffic_index.png"
        )
        return PlotUtils.write(chart_path)
