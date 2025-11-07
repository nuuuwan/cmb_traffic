import os
import time
from dataclasses import dataclass

from selenium import webdriver
from utils import File, JSONFile, Log, Time, TimeDelta, TimeFormat

from cmb_traffic.JourneyRoute import JourneyRoute

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

    @staticmethod
    def parse_time_duration_min(duration_str: str) -> int:
        if " hr " in duration_str:
            hr_str, min_str = duration_str.split(" hr ")
            hours = int(hr_str)
            minutes = int(min_str[:-4]) if min_str.endswith(" min") else 0
            return hours * 60 + minutes * 60

        if " min" in duration_str:
            minutes = int(duration_str[:-4])
            return minutes

        raise ValueError(f"Unknown duration format: {duration_str}")

    @staticmethod
    def parse_distance_km(distance_str: str) -> float:
        if distance_str.endswith(" km"):
            return float(distance_str[:-3])
        raise ValueError(f"Unknown distance format: {distance_str}")

    def get_journey_info(self) -> dict:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1080,1080")

        driver = webdriver.Chrome(options=options)

        log.debug(f"🌐 {self.route.url}")
        driver.get(self.route.url)
        time.sleep(5)

        driver.save_screenshot(self.route.temp_screenshot_path)
        log.debug(f"wrote {File(self.route.temp_screenshot_path)}")

        div_duration = driver.find_element(
            "xpath",
            '//div[contains(@class, "fontHeadlineSmall")]',
        )
        assert div_duration is not None, "Duration div not found"
        duration_str = div_duration.text
        log.debug(f"{duration_str=}")
        duration_min = self.parse_time_duration_min(duration_str)
        log.debug(f"{duration_min=}")

        distance_str = None
        for div_distance in driver.find_elements(
            "xpath",
            '//div[contains(@class, "fontBodyMedium")]',
        ):
            try:
                div_distance_inner = div_distance.find_element(
                    "xpath", ".//div"
                )
            except Exception as e:
                log.error(f"Error finding distance div: {e}")
                continue
            distance_str = div_distance_inner.text
            if distance_str.endswith(" km"):
                break
        assert distance_str is not None, "Distance div not found"
        log.debug(f"{distance_str=}")
        distance_km = self.parse_distance_km(distance_str)
        log.debug(f"{distance_km=}")

        avg_speed_kmph = distance_km / (duration_min / 60)

        driver.quit()

        return dict(
            duration_min=duration_min,
            distance_km=distance_km,
            avg_speed_kmph=avg_speed_kmph,
        )

    def write_journey_info(self) -> TimeDelta:
        d = (
            self.route.to_dict()
            | dict(
                start_time=self.start_time.ut,
            )
            | self.get_journey_info()
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
