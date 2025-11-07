import os
from dataclasses import dataclass
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from utils import File, JSONFile, LatLng, Log

log = Log("JourneyRoute")


@dataclass
class JourneyRoute:
    name: str
    start_latlng: LatLng
    end_latlng: LatLng

    DIR_DATA = "data"
    DIR_DATA_JOURNEYS = os.path.join("data", "journeys")
    DIR_IMAGES = os.path.join("images")

    @property
    def id(self) -> str:
        return self.name.replace(" ", "-").lower()

    @property
    def url(self) -> str:
        return (
            "https://www.google.com/maps/dir"
            + f"/{self.start_latlng.lat:.5f},{self.start_latlng.lng:.5f}"
            + f"/{self.end_latlng.lat:.5f},{self.end_latlng.lng:.5f}/"
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
            start_latlng=(self.start_latlng.lat, self.start_latlng.lng),
            end_latlng=(self.end_latlng.lat, self.end_latlng.lng),
        )

    def reverse(self) -> "JourneyRoute":
        tokens = self.name.split(" to ")
        assert len(tokens) == 2
        start_name, end_name = tokens
        return JourneyRoute(
            name=f"{end_name} to {start_name}",
            start_latlng=self.end_latlng,
            end_latlng=self.start_latlng,
        )

    @property
    def temp_screenshot_path(self):
        return f"screenshot-{self.id}.png"

    def get_duration_data_list(self) -> list[dict]:
        data_list = []
        for file_name in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, file_name)
            data = JSONFile(file_path).read()
            data_list.append(data)
        return data_list

    def compute_index_data_list(self) -> float:
        d_list = self.get_duration_data_list()
        if not d_list:
            return 0.0
        durations = [d["duration"] for d in d_list]
        min_duration = min(durations)
        index_d_list = []
        for d in d_list:
            d = dict(
                start_time=d["start_time"],
                duration=d["duration"],
                index=d["duration"] / min_duration,
            )
            index_d_list.append(d)
        return index_d_list

    def build_chart(self):
        d_list = self.get_duration_data_list()
        d_list.sort(key=lambda d: d["start_time"])

        start_times = [
            datetime.fromtimestamp(d["start_time"]) for d in d_list
        ]
        durations_minutes = [d["duration"] / 60 for d in d_list]

        # Get reverse journey data
        reverse_route = self.reverse()
        reverse_d_list = reverse_route.get_duration_data_list()
        reverse_d_list.sort(key=lambda d: d["start_time"])

        reverse_start_times = [
            datetime.fromtimestamp(d["start_time"]) for d in reverse_d_list
        ]
        reverse_durations_minutes = [
            d["duration"] / 60 for d in reverse_d_list
        ]

        plt.figure(figsize=(16, 9))
        plt.plot(
            start_times,
            durations_minutes,
            marker="o",
            linewidth=2,
            markersize=4,
            label=self.name,
        )
        plt.plot(
            reverse_start_times,
            reverse_durations_minutes,
            marker="s",
            linewidth=2,
            markersize=4,
            label=reverse_route.name,
        )

        # Format x-axis as dates
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        plt.xlabel("Time")
        plt.ylabel("Duration (minutes)")
        plt.title(f"{self.name}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(self.DIR_IMAGES, f"chart-{self.id}.png")
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        plt.close()
        log.info(f"Wrote {File(chart_path)}")

        return chart_path
