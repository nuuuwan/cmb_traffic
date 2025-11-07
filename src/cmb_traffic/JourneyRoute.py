import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import File, JSONFile, LatLng, Log

log = Log("JourneyRoute")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


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
            + f"/{self.start_latlng.lat:.6f},{self.start_latlng.lng:.6f}"
            + f"/{self.end_latlng.lat:.6f},{self.end_latlng.lng:.6f}/"
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

    def get_journey_data_list(self) -> list[dict]:
        data_list = []
        for file_name in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, file_name)
            data = JSONFile(file_path).read()
            data_list.append(data)
        return data_list

    def build_chart(self):
        d_list = self.get_journey_data_list()
        d_list.sort(key=lambda d: d["start_time"])

        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=LK_TZ) for d in d_list
        ]
        avg_speed_kmphs = [d["avg_speed_kmph"] for d in d_list]

        reverse_route = self.reverse()
        reverse_d_list = reverse_route.get_journey_data_list()
        reverse_d_list.sort(key=lambda d: d["start_time"])

        reverse_start_times = [
            datetime.fromtimestamp(d["start_time"], tz=LK_TZ)
            for d in reverse_d_list
        ]
        reverse_avg_speed_kmphs = [d["avg_speed_kmph"] for d in reverse_d_list]

        plt.figure(figsize=(8, 4.5))
        plt.plot(
            start_times,
            avg_speed_kmphs,
            marker="o",
            linewidth=2,
            markersize=4,
            label=self.name,
        )
        plt.plot(
            reverse_start_times,
            reverse_avg_speed_kmphs,
            marker="s",
            linewidth=2,
            markersize=4,
            label=reverse_route.name,
        )

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Time")
        plt.ylabel("Average Speed (km/h)")
        plt.title(f"{self.name}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(self.DIR_IMAGES, f"chart-{self.id}.png")
        plt.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close()
        log.info(f"Wrote {File(chart_path)}")

        return chart_path
