import os
from datetime import datetime

import matplotlib.pyplot as plt

from cmb_traffic.readme.ReadMeIndexChartUtilsMixin import \
    ReadMeIndexChartUtilsMixin
from utils_future import PlotUtils, TimeUtils


class ReadMeIndexChartTTRMixin(ReadMeIndexChartUtilsMixin):
    def build_ttr_chart(self, journey_d_list):
        plt.close()
        journey_d_list = self.filter_to_chart_days(journey_d_list)
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

        period_label = self.get_period_label(journey_d_list)
        plt.xlabel("Start Time")
        plt.ylabel("Travel Time Ratio (TTR)")
        plt.title(f"{self.title} as Travel Time Ratio (TTR)\n{period_label}")

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, f"{self.id}.ttr_traffic_index.png"
        )
        return PlotUtils.write(chart_path), current_ttr_value
