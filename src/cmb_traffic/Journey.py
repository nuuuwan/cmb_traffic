import os
import time
from dataclasses import dataclass

from selenium import webdriver
from utils import JSONFile, Log, Time, TimeDelta, TimeFormat

from cmb_traffic.JourneyRoute import JourneyRoute

log = Log("Journey")


@dataclass
class Journey:
    route: JourneyRoute
    start_time: Time

    @property
    def data_path(self):
        return os.path.join(
            self.route.dir_path,
            TimeFormat.TIME_ID.format(self.start_time),
        )

    @staticmethod
    def parse_time_duration(duration_str: str) -> TimeDelta:
        if duration_str.endswith(" min"):
            minutes = int(duration_str[:-4])
            return TimeDelta(minutes * 60)
        raise ValueError(f"Unknown duration format: {duration_str}")

    def get_duration(self) -> TimeDelta:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1920")

        driver = webdriver.Chrome(options=options)

        log.debug(f"🌐 {self.route.url}")
        driver.get(self.route.url)
        time.sleep(5)
        driver.save_screenshot(self.route.temp_screenshot_path)

        div_duration = driver.find_element(
            "xpath",
            '//div[contains(@class, "fontHeadlineSmall")]',
        )
        assert div_duration is not None, "Duration div not found"
        duration_str = div_duration.text
        log.debug(f"{duration_str=}")

        driver.quit()
        duration = self.parse_time_duration(duration_str)
        return duration

    def write_duration(self) -> TimeDelta:
        d = self.route.to_dict() | dict(
            start_time=self.start_time.ut,
            duration=self.get_duration().dut,
        )
        os.makedirs(self.route.dir_path, exist_ok=True)
        json_file = JSONFile(self.data_path)
        json_file.write(d)
        log.debug(f"Wrote {json_file}")

    @staticmethod
    def from_route_now(route):
        return Journey(
            route=route,
            start_time=Time.now(),
        )
