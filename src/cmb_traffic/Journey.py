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

    def get_duration(self) -> TimeDelta:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1920")

        driver = webdriver.Chrome(options=options)

        driver.get(self.url)
        time.sleep(5)
        driver.save_screenshot("screenshot.png")
        driver.quit()
