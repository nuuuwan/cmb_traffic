from dataclasses import dataclass

from utils import File, Log

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute

log = Log("TrafficIndex")


@dataclass
class TrafficIndex:
    undirected_journey_route_list: list[JourneyRoute]

    README_PATH = "README.md"

    def get_full_journey_route_list(self) -> list[JourneyRoute]:
        return self.undirected_journey_route_list + [
            route.reverse() for route in self.undirected_journey_route_list
        ]

    def write_all(self):
        for route in self.get_full_journey_route_list():
            journey = Journey.from_route_now(route)
            journey.write_duration()

    def get_lines_for_routes(self) -> list[str]:
        lines = ["## Routes", ""]
        for route in self.undirected_journey_route_list:
            lines.extend([f"### {route.name}", ""])
            chart_path = route.build_chart()
            lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines

    def build_readme(self):
        lines = [
            "# Colombo Traffic Index (cmb_traffic)",
            "",
        ] + self.get_lines_for_routes()
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
