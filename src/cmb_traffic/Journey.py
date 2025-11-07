import os
import time
from dataclasses import dataclass

from selenium import webdriver
from utils import JSONFile, LatLng, Log, Time, TimeDelta, TimeFormat

log = Log("Journey")


@dataclass
class Journey:
    name: str
    start_latlng: LatLng
    end_latlng: LatLng
    start_time: Time

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
    def name_data_path(self) -> str:
        return os.path.join(
            self.DIR_DATA_JOURNEYS,
            self.name.replace(" ", "-"),
        )

    @property
    def data_path(self):
        return os.path.join(
            self.name_data_path,
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

        log.debug(f"🌐 {self.url}")
        driver.get(self.url)
        time.sleep(5)
        driver.save_screenshot("screenshot.png")

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
        d = dict(
            name=self.name,
            start_latlng=(self.start_latlng.lat, self.start_latlng.lng),
            end_latlng=(self.end_latlng.lat, self.end_latlng.lng),
            start_time=self.start_time.ut,
            duration=self.get_duration().dut,
        )

        os.makedirs(self.name_data_path, exist_ok=True)
        json_file = JSONFile(self.data_path)
        json_file.write(d)
        log.debug(f"Wrote {json_file}")
