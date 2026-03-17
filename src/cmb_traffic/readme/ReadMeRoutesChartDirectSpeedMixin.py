import os
from datetime import datetime

import matplotlib.pyplot as plt

from cmb_traffic.Journey import Journey
from cmb_traffic.readme.ReadMeIndexChartUtilsMixin import \
    ReadMeIndexChartUtilsMixin
from utils_future import PlotUtils


class ReadMeRoutesChartDirectSpeedMixin(ReadMeIndexChartUtilsMixin):
    def __get_chart_data__(self, route):
        journey_list = Journey.list_all_for_route(route)
        if journey_list:
            max_ut_start = max(j.ut_start for j in journey_list)
            cutoff_ut = max_ut_start - self.DEFAULT_CHART_DAYS * 86400
            journey_list = [
                j for j in journey_list if j.ut_start >= cutoff_ut
            ]
        start_times = [
            datetime.fromtimestamp(j.ut_start) for j in journey_list
        ]
        direct_speed_kmphs = [j.direct_speed_kmph for j in journey_list]
        return (start_times, direct_speed_kmphs)

    def build_chart_for_route(self, route):
        plt.close()
        (start_times, direct_speed_kmphs) = self.__get_chart_data__(route)
        reverse_route = route.reverse()
        (reverse_start_times, reverse_direct_speed_kmphs) = (
            self.__get_chart_data__(reverse_route)
        )

        plt.figure(figsize=(8, 4.5))
        for x_data, y_data, label in [
            (start_times, direct_speed_kmphs, route.name),
            (
                reverse_start_times,
                reverse_direct_speed_kmphs,
                reverse_route.name,
            ),
        ]:
            plt.plot(
                x_data,
                y_data,
                linewidth=2,
                label=label,
            )

        plt.xlabel("Time")
        plt.ylabel("Direct Speed (km/h)")
        plt.title(f"{route.name.replace(' to ', ' ↔ ')}")

        os.makedirs(route.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(route.DIR_IMAGES, f"route.{route.id}.png")
        return PlotUtils.write(chart_path)
