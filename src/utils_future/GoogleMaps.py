import time

from selenium import webdriver
from utils import Log

from utils_future import LatLng

log = Log("GoogleMaps")


class GoogleMaps:

    @staticmethod
    def __parse_time_duration_min_str__(duration_str: str) -> int:
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
    def __parse_time_duration_min__(driver) -> int:
        div_duration = driver.find_element(
            "xpath",
            '//div[contains(@class, "fontHeadlineSmall")]',
        )
        assert div_duration is not None, "Duration div not found"
        duration_str = div_duration.text
        return GoogleMaps.__parse_time_duration_min_str__(duration_str)

    @staticmethod
    def __parse_distance_km_str__(distance_str: str) -> float:
        if distance_str.endswith(" km"):
            return float(distance_str[:-3])
        raise ValueError(f"Unknown distance format: {distance_str}")

    @staticmethod
    def __parse_distance_km__(driver) -> float:
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
        return GoogleMaps.__parse_distance_km_str__(distance_str)

    @staticmethod
    def get_url_for_line(start_latlng: LatLng, end_latlng: LatLng) -> str:
        return (
            "https://www.google.com/maps/dir"
            + f"/{start_latlng.lat:.6f},{start_latlng.lng:.6f}"
            + f"/{end_latlng.lat:.6f},{end_latlng.lng:.6f}/"
        )

    @staticmethod
    def get_url_for_point(latlng: LatLng) -> str:
        return (
            "https://www.google.com/maps/place"
            + f"/{latlng.lat:.6f},{latlng.lng:.6f}/"
        )

    @staticmethod
    def __get_driver__() -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1080,1080")
        driver = webdriver.Chrome(options=options)
        return driver

    @staticmethod
    def __get_journey_info_single_(
        start_latlng: LatLng, end_latlng: LatLng, t_sleep: int
    ) -> dict:
        driver = GoogleMaps.__get_driver__()
        url = GoogleMaps.get_url_for_line(start_latlng, end_latlng)
        log.debug(f"🌐 {url}")
        driver.get(url)
        time.sleep(t_sleep)

        duration_min = GoogleMaps.__parse_time_duration_min__(driver)
        distance_km = GoogleMaps.__parse_distance_km__(driver)
        avg_speed_kmph = distance_km / (duration_min / 60)

        direct_distance_km = start_latlng.distance(end_latlng)
        direct_speed_kmph = direct_distance_km / (duration_min / 60)

        driver.quit()

        return dict(
            duration_min=duration_min,
            distance_km=distance_km,
            avg_speed_kmph=avg_speed_kmph,
            direct_distance_km=direct_distance_km,
            direct_speed_kmph=direct_speed_kmph,
        )

    @staticmethod
    def get_journey_info(start_latlng: LatLng, end_latlng: LatLng) -> dict:
        t_wait = 1
        multiplier = 2
        max_t_wait = 60
        while True:
            try:
                return GoogleMaps.__get_journey_info_single_(
                    start_latlng, end_latlng, t_sleep=t_wait * 3
                )
            except Exception as e:
                log.warning(f"Error getting journey info: {e}. ")
                if t_wait > max_t_wait:
                    log.error("Max wait time exceeded. Aborting.")
                    raise e
                log.debug(f"Waiting {t_wait} seconds before retrying.")
                time.sleep(t_wait)
                t_wait *= multiplier
