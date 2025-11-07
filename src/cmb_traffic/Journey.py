import time
from dataclasses import dataclass

from selenium import webdriver
from utils import LatLng, Log, Time, TimeDelta

log = Log("Journey")


@dataclass
class Journey:
    name: str
    start_latlng: LatLng
    end_latlng: LatLng
    start_time: Time

    @property
    def url(self) -> str:
        return (
            "https://www.google.com/maps/dir"
            + f"/{self.start_latlng.lat:.5f},{self.start_latlng.lng:.5f}"
            + f"/{self.end_latlng.lat:.5f},{self.end_latlng.lng:.5f}/"
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

        driver.get(self.url)
        time.sleep(5)
        driver.save_screenshot("screenshot.png")

        # div where class contains fontHeadlineSmall
        div_duration = driver.find_element(
            "xpath",
            '//div[contains(@class, "fontHeadlineSmall")]',
        )
        assert div_duration is not None, "Duration div not found"
        duration_str = div_duration.text

        driver.quit()
        duration = self.parse_time_duration(duration_str)
        return duration
