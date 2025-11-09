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
            "## 📊 About This Index",
            "",
            "The Colombo Traffic Index (CTI) provides a real-time measure of "
            "traffic congestion across key routes in Colombo. By tracking "
            "average travel speeds throughout the day, this index helps:",
            "",
            "- 🚗 **Commuters** plan their travel times and identify optimal "
            "departure windows",
            "- 📈 **Researchers** analyze traffic patterns and urban mobility "
            "trends",
            "- 🏛️ **Policy makers** make data-driven decisions on "
            "infrastructure and traffic management",
            "",
        ]
        return lines

    def get_lines_for_methodology(self) -> list[str]:
        return [
            "### Methodology",
            "",
            "We monitor a set of representative routes across Colombo City, "
            "measuring travel times and speeds at regular intervals "
            "throughout the day using the Google Maps. "
            "",
            "Each route is monitored in both directions to capture "
            "bidirectional traffic patterns, as congestion levels often "
            "differ significantly based on travel direction and time of day.",
            "",
            "#### Data Collection",
            "",
            "- Routes are sampled from Google Maps throughout the day",
            "- Travel time, distance, and average speed are recorded for "
            "each journey",
            "- Data is timestamped with Sri Lanka timezone (UTC+5:30)",
            "- Historical data is accumulated to establish baseline patterns",
            "",
            "#### Analysis",
            "",
            "- The overall traffic condition is assessed by calculating the "
            "average speed across all monitored routes at each time point",
            "- Free-flow speeds are determined from the fastest observed "
            "travel times for each route in the last 24 hours",
            "- Peak congestion periods are identified by comparing current "
            "speeds against baseline free-flow speeds",
            "",
        ]

    def get_lines_for_ttr(self) -> list[str]:
        return [
            "### Travel Time Ratio (TTR)",
            "",
            "We also track the **Travel Time Ratio (TTR)** for each route, "
            "which measures congestion severity:",
            "",
            "```python",
            "TTR = Peak Hour Travel Time / Free Flow Travel Time",
            "    = Free Flow Speed / Peak Hour Speed",
            "```",
            "",
            "A TTR of 1.0 indicates free-flow conditions, while higher "
            "values indicate increasing congestion. For example, a TTR of "
            "2.0 means travel takes twice as long during peak hours compared "
            "to free-flow conditions.",
            "",
            "Lower average speeds indicate heavier traffic congestion, "
            "while higher speeds suggest free-flow conditions. By tracking "
            "these patterns over time, we can identify peak congestion "
            "periods and seasonal trends.",
            "",
        ]

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
            + self.get_lines_for_methodology()
            + self.get_lines_for_ttr()
            + self.get_lines_for_index(journey_d_list)
            + self.get_lines_for_routes()
            + self.get_lines_for_footer()
        )
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
