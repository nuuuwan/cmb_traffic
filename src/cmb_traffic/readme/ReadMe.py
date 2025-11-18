from utils import File, Format, Log, Time, TimeFormat

from cmb_traffic.Journey import Journey
from cmb_traffic.readme.ReadMeIndexMixin import ReadMeIndexMixin
from cmb_traffic.readme.ReadMeRoutesMixin import ReadMeRoutesMixin
from cmb_traffic.Route import Route

log = Log("ReadMe")


class ReadMe(ReadMeRoutesMixin, ReadMeIndexMixin):

    DIR_IMAGES = Route.DIR_IMAGES
    DEFAULT_README_PATH = "README.md"

    def __init__(self, traffic_index):
        self.traffic_index = traffic_index

    @property
    def id(self) -> str:
        return self.traffic_index.id

    @property
    def title(self) -> str:
        return self.traffic_index.title

    @property
    def readme_path(self) -> str:
        return f"README.{self.id}.md"

    def get_lines_for_header(self) -> list[str]:
        time_last_updated = Journey.get_time_last_updated()
        time_last_updated_for_badge = Format.badge(
            TimeFormat.TIME.format(Time(time_last_updated))
        )
        return [
            f"# 🇱🇰 {self.title}",
            "",
            self.traffic_index.description,
            "",
            "![LatestEstimateFor](https://img.shields.io/badge"
            + f"/latest_estimate_for-{time_last_updated_for_badge}-green)",
            "",
        ]

    def get_lines_for_about(self) -> list[str]:
        lines = [
            "## Definitions, Vision and Big-Picture",
            "",
            "See [The Colombo Traffic Index (CTI) - "
            + "Understanding the Bigger Picture](README.VISION.md)",
            "",
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
        journey_d_list = self.traffic_index.get_journey_data_list()
        if not journey_d_list:
            log.warning(
                f"No journey data for {self.traffic_index.title}, "
                + "skipping README generation"
            )
            return
        lines = (
            self.get_lines_for_header()
            + self.get_lines_for_about()
            + self.get_lines_for_cti(journey_d_list)
            + self.get_lines_for_routes()
            + self.get_lines_for_footer()
        )
        readme_file = File(self.readme_path)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")

        if self.traffic_index.is_default:
            default_readme_file = File(self.DEFAULT_README_PATH)
            default_readme_file.write_lines(lines)
            log.info(f"Wrote {default_readme_file}")
