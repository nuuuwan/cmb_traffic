import os
from dataclasses import dataclass

from utils import LatLng


@dataclass
class JourneyRoute:
    name: str
    start_latlng: LatLng
    end_latlng: LatLng

    DIR_DATA = "data"
    DIR_DATA_JOURNEYS = os.path.join("data", "journeys")

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

    def transpose(self) -> "JourneyRoute":
        return JourneyRoute(
            name=self.name + " (Reversed)",
            start_latlng=self.end_latlng,
            end_latlng=self.start_latlng,
        )
