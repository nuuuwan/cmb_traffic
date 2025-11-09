import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import matplotlib.pyplot as plt
from utils import JSONFile, Log

from cmb_traffic.Location import Location
from utils_future import GoogleMaps, PlotUtils

log = Log("JourneyRoute")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


@dataclass
class JourneyRoute:
    start_location: Location
    end_location: Location

    DIR_DATA = "data"
    DIR_DATA_JOURNEYS = os.path.join("data", "journeys")
    DIR_IMAGES = os.path.join("images")

    @property
    def name(self) -> str:
        return f"{self.start_location.name} to {self.end_location.name}"

    @property
    def name_bidirectional(self) -> str:
        return f"{self.start_location.name} ↔ {self.end_location.name}"

    @property
    def id(self) -> str:
        return self.name.replace(" ", "-").lower()

    @property
    def url(self) -> str:
        return GoogleMaps.get_url(
            self.start_location.latlng,
            self.end_location.latlng,
        )

    @property
    def dir_path(self) -> str:
        return os.path.join(
            self.DIR_DATA_JOURNEYS,
            self.name.replace(" ", "-"),
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            start_location=self.start_location.to_dict(),
            end_location=self.end_location.to_dict(),
        )

    def reverse(self) -> "JourneyRoute":
        return JourneyRoute(
            start_location=self.end_location,
            end_location=self.start_location,
        )

    @property
    def temp_screenshot_path(self):
        return f"screenshot-{self.id}.png"

    def get_journey_data_list(self) -> list[dict]:
        data_list = []
        for root, _, files in os.walk(self.dir_path):
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    data = JSONFile(file_path).read()
                    data_list.append(data)
        return data_list

    def __get_chart_data__(self):
        d_list = self.get_journey_data_list()
        d_list.sort(key=lambda d: d["start_time"])
        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=LK_TZ) for d in d_list
        ]
        avg_speed_kmphs = [d["avg_speed_kmph"] for d in d_list]

        return (
            start_times,
            avg_speed_kmphs,
        )

    def build_chart(self):
        (start_times, avg_speed_kmphs) = self.__get_chart_data__()
        reverse_route = self.reverse()
        (reverse_start_times, reverse_avg_speed_kmphs) = (
            reverse_route.__get_chart_data__()
        )

        plt.figure(figsize=(8, 4.5))
        for x_data, y_data, label in [
            (start_times, avg_speed_kmphs, self.name),
            (
                reverse_start_times,
                reverse_avg_speed_kmphs,
                reverse_route.name,
            ),
        ]:
            plt.plot(
                x_data,
                y_data,
                marker="o" if label == self.name else "s",
                linewidth=2,
                markersize=4,
                label=label,
            )

        plt.xlabel("Time")
        plt.ylabel("Average Speed (km/h)")
        plt.title(
            f"{self.name.replace(" to ", " ↔ ")} - Average Speed Over Time"
        )

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(self.DIR_IMAGES, f"chart-{self.id}.png")
        return PlotUtils.write(chart_path)
