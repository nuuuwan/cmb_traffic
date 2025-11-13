import os
from dataclasses import dataclass
from datetime import timedelta, timezone

from utils import Log

from cmb_traffic.Location import Location
from utils_future import GoogleMaps

log = Log("Route")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


@dataclass
class Route:
    start_location: Location
    end_location: Location

    DIR_DATA = "data"

    DIR_IMAGES = os.path.join("images")

    def is_location_order_north_south(self) -> bool:
        return self.start_location.latlng.lat >= self.end_location.latlng.lat

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
        return GoogleMaps.get_url_for_line(
            self.start_location.latlng,
            self.end_location.latlng,
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            start_location=self.start_location.to_dict(),
            end_location=self.end_location.to_dict(),
        )

    @classmethod
    def from_dict(cls, d):
        return cls(
            start_location=Location.from_dict(d["start_location"]),
            end_location=Location.from_dict(d["end_location"]),
        )

    def reverse(self) -> "Route":
        return Route(
            start_location=self.end_location,
            end_location=self.start_location,
        )

    @property
    def temp_screenshot_path(self):
        return f"screenshot-{self.id}.png"

    def to_dict_flat(self) -> dict:
        return self.start_location.to_dict_flat(
            prefix="start"
        ) | self.end_location.to_dict_flat(prefix="end")
