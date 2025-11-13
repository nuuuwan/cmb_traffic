import math
from dataclasses import dataclass

import geopy.distance
from utils import Parse


@dataclass
class LatLng:
    lat: float
    lng: float

    def __eq__(self, other):
        return self.lat == other.lat and self.lng == other.lng

    def __hash__(self):
        return hash((self.lat, self.lng))

    def __str__(self):
        lat_str = f"{abs(self.lat):.6f}°" + ("N" if self.lat > 0 else "S")
        lng_str = f"{abs(self.lng):.6f}°" + ("E" if self.lng > 0 else "W")
        return f"{lat_str}, {lng_str}"

    def __repr__(self):
        return str(self)

    @classmethod
    def from_dict(cls, d):
        return cls(
            lat=d["lat"],
            lng=d["lng"],
        )

    @classmethod
    def from_tuple(cls, t):
        return cls(
            lat=t[0],
            lng=t[1],
        )

    @staticmethod
    def parse(latlng_str_original: str) -> str:
        latlng_str = latlng_str_original.replace("°", " ").strip()
        for x in ["N", "S", "E", "W"]:
            latlng_str = latlng_str.replace(x, "")
        lat_str, lng_str = latlng_str.split(",")
        lat = Parse.float(lat_str) * (-1 if "S" in latlng_str_original else 1)
        lng = Parse.float(lng_str) * (-1 if "W" in latlng_str_original else 1)
        return LatLng(lat, lng)

    def distance(self, other: "LatLng") -> float:
        return geopy.distance.geodesic(
            (self.lat, self.lng), (other.lat, other.lng)
        ).km

    def angle(self, other: "LatLng") -> float:
        return (
            math.atan2(other.lat - self.lat, other.lng - self.lng)
            * 180
            / math.pi
        )

    @staticmethod
    def bbox(latlng_list: list["LatLng"]) -> tuple["LatLng"]:
        lat_list = [latlng.lat for latlng in latlng_list]
        lng_list = [latlng.lng for latlng in latlng_list]
        return (
            LatLng(min(lat_list), min(lng_list)),
            LatLng(max(lat_list), max(lng_list)),
        )

    @staticmethod
    def get_func_t(
        latlng_list: list["LatLng"],
        width: float,
        height: float,
        padding: float,
    ) -> callable:
        width_actual = width - padding * 2
        height_actual = height - padding * 2

        (min_latlng, max_latlng) = LatLng.bbox(latlng_list)

        def t(latlng):
            x = (latlng.lng - min_latlng.lng) / (
                max_latlng.lng - min_latlng.lng
            )
            y = (latlng.lat - min_latlng.lat) / (
                max_latlng.lat - min_latlng.lat
            )
            return (
                x * width_actual + padding,
                (1 - y) * height_actual + padding,
            )

        return t
