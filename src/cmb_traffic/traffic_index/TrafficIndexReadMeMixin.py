from utils import File, Format, Log, Time, TimeFormat

from cmb_traffic.JourneyRoute import JourneyRoute
from cmb_traffic.traffic_index.TrafficIndexReadMeIndexMixin import \
    TrafficIndexReadMeIndexMixin
from cmb_traffic.traffic_index.TrafficIndexReadMeRoutesMixin import \
    TrafficIndexReadMeRoutesMixin

log = Log("TrafficIndexReadMeMixin")


class TrafficIndexReadMeMixin(
    TrafficIndexReadMeRoutesMixin, TrafficIndexReadMeIndexMixin
):

    DIR_IMAGES = JourneyRoute.DIR_IMAGES
    README_PATH = "README.md"

    @staticmethod
    def get_time_updated_for_badge(journey_d_list) -> str:

        time_updated = max([d["start_time"] for d in journey_d_list])
        time_updated_for_badge = Format.badge(
            TimeFormat.TIME.format(Time(time_updated))
        )
        return time_updated_for_badge

    def get_lines_for_header(self, journey_d_list) -> list[str]:
        time_updated_for_badge = self.get_time_updated_for_badge(
            journey_d_list
        )
        return [
            "# 🇱🇰 Colombo Traffic Index (cmb_traffic)",
            "",
            "![LatestEstimateFor](https://img.shields.io/badge"
            + f"/latest_estimate_for-{time_updated_for_badge}-green)",
            "",
        ]

    def get_lines_for_about(self) -> list[str]:
        lines = [
            "## Definitions, Vision and Big-Picture",
            "",
            "See [The Colombo Traffic Index (CTI) - "
            + "Understanding the Bigger Picture](README.VISION.md)",
        ]
        return lines

    def get_lines_for_footer(self) -> list[str]:
        return [
            "![Maintainer]"
            + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
            "![MadeWith]"
            + "(https://img.shields.io/badge/made_with-python-blue)",
            "[![License: MIT]"
            + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
            + "(https://opensource.org/licenses/MIT)",
            "",
        ]

    def build_readme(self):
        journey_d_list = self.get_journey_data_list()
        lines = (
            self.get_lines_for_header(journey_d_list)
            + self.get_lines_for_about()
            + self.get_lines_for_cti(journey_d_list)
            + self.get_lines_for_routes()
            + self.get_lines_for_footer()
        )
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
