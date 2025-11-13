import os
from dataclasses import asdict, dataclass
from typing import Generator

from utils import JSONFile, Log, Time, TimeFormat

from cmb_traffic.Route import Route
from utils_future import GoogleMaps

log = Log("Journey")


@dataclass
class Journey:
    route: Route
    ut_start: int
    duration_min: float
    distance_km: float
    avg_speed_kmph: float
    direct_distance_km: float
    direct_speed_kmph: float

    ROUND_FACTOR = 1_800
    DIR_DATA_JOURNEYS = os.path.join("data", "journeys")

    @property
    def data_path(self):
        time_id = TimeFormat.TIME_ID.format(Time(self.ut_start))
        year = time_id[:4]
        month = time_id[:6]
        date = time_id[:8]
        data_dir = os.path.join(
            self.route.dir_path,
            year,
            month,
            date,
        )
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(
            data_dir,
            f"{time_id}.json",
        )

    @staticmethod
    def from_route(route):
        ut = Time.now().ut
        ut_rounded = round(ut / Journey.ROUND_FACTOR) * Journey.ROUND_FACTOR
        google_maps_info = GoogleMaps.get_journey_info(
            route.start_location.latlng, route.end_location.latlng
        )
        return Journey(
            route=route,
            ut_start=ut_rounded,
            duration_min=google_maps_info["duration_min"],
            distance_km=google_maps_info["distance_km"],
            avg_speed_kmph=google_maps_info["avg_speed_kmph"],
            direct_distance_km=google_maps_info["direct_distance_km"],
            direct_speed_kmph=google_maps_info["direct_speed_kmph"],
        )

    @classmethod
    def from_dict(cls, d):
        return cls(
            route=Route.from_dict(d),
            ut_start=d["ut_start"],
            duration_min=d["duration_min"],
            distance_km=d["distance_km"],
            avg_speed_kmph=d["avg_speed_kmph"],
            direct_distance_km=d["direct_distance_km"],
            direct_speed_kmph=d["direct_speed_kmph"],
        )

    @classmethod
    def from_file(cls, file_path: str) -> "Journey":
        json_file = JSONFile(file_path)
        d = json_file.read()
        return cls.from_dict(d)

    @classmethod
    def __gen_file_paths__(cls) -> Generator[str, None, None]:
        for root, _, files in os.walk(cls.DIR_DATA_JOURNEYS):
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    yield file_path

    @classmethod
    def list_all(cls) -> list["Journey"]:
        journey_list = []
        for file_path in cls.__gen_file_paths__():
            journey = cls.from_file(file_path)
            journey_list.append(journey)
        return journey_list

    def write(self):
        json_file = JSONFile(self.data_path)
        json_file.write(asdict(self))
        log.debug(f"Wrote {json_file}")
