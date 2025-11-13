import os
from dataclasses import asdict, dataclass
from typing import Generator

from utils import JSONFile, Log, Time, TimeFormat, TSVFile

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
    ALL_DATA_PATH = os.path.join("data", "all_journeys.tsv")

    @classmethod
    def __get_dir_path_for_route__(cls, route: Route) -> str:
        return os.path.join(
            cls.DIR_DATA_JOURNEYS,
            route.name.replace(" ", "-"),
        )

    @property
    def data_path(self):
        time_id = TimeFormat.TIME_ID.format(Time(self.ut_start))
        year = time_id[:4]
        month = time_id[:6]
        date = time_id[:8]
        data_dir = os.path.join(
            self.__get_dir_path_for_route__(self.route),
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
            route=Route.from_dict(d["route"]),
            ut_start=d["ut_start"],
            duration_min=d["duration_min"],
            distance_km=d["distance_km"],
            avg_speed_kmph=d["avg_speed_kmph"],
            direct_distance_km=d["direct_distance_km"],
            direct_speed_kmph=d["direct_speed_kmph"],
        )

    @classmethod
    def from_file_path(cls, file_path: str) -> "Journey":
        json_file = JSONFile(file_path)
        d = json_file.read()
        return cls.from_dict(d)

    @classmethod
    def __gen_file_paths_for_dir_path__(
        cls, dir_path
    ) -> Generator[str, None, None]:
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    yield file_path

    @classmethod
    def __list_all_for_dir_path__(cls, dir_path: str) -> list["Journey"]:
        journey_list = []
        for file_path in cls.__gen_file_paths_for_dir_path__(dir_path):
            journey = cls.from_file_path(file_path)
            journey_list.append(journey)
        journey_list.sort(key=lambda journey: journey.ut_start)
        return journey_list

    @classmethod
    def list_all(cls) -> list["Journey"]:
        return cls.__list_all_for_dir_path__(cls.DIR_DATA_JOURNEYS)

    @classmethod
    def list_all_for_route(cls, route: Route) -> str:
        dir_path = cls.__get_dir_path_for_route__(route)
        return cls.__list_all_for_dir_path__(dir_path)

    def write(self):
        json_file = JSONFile(self.data_path)
        json_file.write(asdict(self))
        log.debug(f"Wrote {json_file}")

    def to_dict_flat(self) -> dict:
        return self.route.to_dict_flat() | dict(
            ut_start=self.ut_start,
            duration_min=self.duration_min,
            distance_km=self.distance_km,
            avg_speed_kmph=self.avg_speed_kmph,
            direct_distance_km=self.direct_distance_km,
            direct_speed_kmph=self.direct_speed_kmph,
        )

    @classmethod
    def write_all(cls):
        journey_list = cls.list_all()
        d_list = [journey.to_dict_flat() for journey in journey_list]
        tsv_file = TSVFile(Journey.ALL_DATA_PATH)
        tsv_file.write(d_list)
        log.info(f"Wrote {tsv_file}")
