import os
from dataclasses import dataclass

from utils import JSONFile, Log, Time, TimeDelta, TimeFormat

from cmb_traffic.JourneyRoute import JourneyRoute
from utils_future import GoogleMaps

log = Log("Journey")


@dataclass
class Journey:
    route: JourneyRoute
    start_time: Time

    ROUND_FACTOR = 1_800

    @property
    def data_path(self):
        time_id = TimeFormat.TIME_ID.format(self.start_time)
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

    def write_journey_info(self) -> TimeDelta:
        d = (
            self.route.to_dict()
            | dict(
                start_time=self.start_time.ut,
            )
            | GoogleMaps.get_journey_info(
                self.route.start_latlng,
                self.route.end_latlng,
            )
        )
        log.debug(f"{d=}")
        os.makedirs(self.route.dir_path, exist_ok=True)
        json_file = JSONFile(self.data_path)
        json_file.write(d)
        log.debug(f"Wrote {json_file}")

    @staticmethod
    def from_route_now(route):
        ut = Time.now().ut
        ut_rounded = round(ut / Journey.ROUND_FACTOR) * Journey.ROUND_FACTOR
        time_rounded = Time(ut_rounded)
        return Journey(
            route=route,
            start_time=time_rounded,
        )
