import time

from selenium import webdriver
from utils import LatLng, Log

log = Log("GoogleMaps")


class GoogleMaps:

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

    @staticmethod
    def get_url(start_latlng: LatLng, end_latlng: LatLng) -> str:
        return (
            "https://www.google.com/maps/dir"
            + f"/{start_latlng.lat:.6f},{start_latlng.lng:.6f}"
            + f"/{end_latlng.lat:.6f},{end_latlng.lng:.6f}/"
        )

    @staticmethod
    def get_journey_info(start_latlng: LatLng, end_latlng: LatLng) -> dict:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1080,1080")

        driver = webdriver.Chrome(options=options)

        url = GoogleMaps.get_url(start_latlng, end_latlng)
        log.debug(f"🌐 {url}")
        driver.get(url)
        time.sleep(5)

        div_duration = driver.find_element(
            "xpath",
            '//div[contains(@class, "fontHeadlineSmall")]',
        )
        assert div_duration is not None, "Duration div not found"
        duration_str = div_duration.text
        duration_min = GoogleMaps.parse_time_duration_min(duration_str)

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
        distance_km = GoogleMaps.parse_distance_km(distance_str)

        avg_speed_kmph = distance_km / (duration_min / 60)

        driver.quit()

        return dict(
            duration_min=duration_min,
            distance_km=distance_km,
            avg_speed_kmph=avg_speed_kmph,
        )
