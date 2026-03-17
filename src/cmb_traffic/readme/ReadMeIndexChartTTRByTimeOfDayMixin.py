import os
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from cmb_traffic.readme.ReadMeIndexChartUtilsMixin import \
    ReadMeIndexChartUtilsMixin
from utils_future import PlotUtils, TimeUtils

log = Log("ReadMe")


class ReadMeIndexChartTTRByTimeOfDayMixin(ReadMeIndexChartUtilsMixin):
    def build_ttr_by_time_of_day_chart(self, journey_d_list):
        plt.close()

        if not journey_d_list:
            return None

        journey_d_list = self.append_ttrs(journey_d_list)

        hour_to_ttrs = defaultdict(list)
        for d in journey_d_list:
            dt = datetime.fromtimestamp(d["ut_start"], tz=TimeUtils.LK_TZ)
            hour = dt.hour
            hour_to_ttrs[hour].append(d["ttr"])

        hours = sorted(hour_to_ttrs.keys())
        avg_ttrs = [
            sum(hour_to_ttrs[h]) / len(hour_to_ttrs[h]) for h in hours
        ]

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
        plt.title(f"{self.title} - Average CTI by Time of Day")

        hour_labels = [
            datetime(2000, 1, 1, h).strftime(PlotUtils.TIME_ONLY_FORMAT)
            for h in range(0, 24, 4)
        ]
        plt.xticks(range(0, 24, 4), hour_labels)

        ax = plt.gca()
        ax.set_xticks(range(0, 24), minor=True)
        plt.grid(True, alpha=0.3, which="major")
        plt.grid(True, alpha=0.1, which="minor")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, f"{self.id}.ttr_by_time_of_day.png"
        )
        plt.tight_layout()
        plt.savefig(chart_path, dpi=150)
        plt.close()
        log.info(f"Wrote chart to {chart_path}")
        return chart_path
