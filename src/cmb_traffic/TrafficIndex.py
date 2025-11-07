import os
from dataclasses import dataclass
from datetime import datetime

import matplotlib.pyplot as plt
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

    def compute_index_data_list(self):
        start_time_to_index = {}
        for route in self.get_full_journey_route_list():
            index_data_list = route.compute_index_data_list()
            for d in index_data_list:
                start_time = d["start_time"]
                index = d["index"]
                if start_time not in start_time_to_index:
                    start_time_to_index[start_time] = []
                start_time_to_index[start_time].append(index)

        overall_index_data_list = []
        for start_time, index_list in start_time_to_index.items():
            n = len(index_list)
            overall_index = sum(index_list) / n
            overall_index_data_list.append(
                dict(start_time=start_time, n=n, index=overall_index)
            )
        overall_index_data_list.sort(key=lambda d: d["start_time"])
        return overall_index_data_list

    def build_index_chart(self):
        index_data_list = self.compute_index_data_list()

        start_times = [
            datetime.fromtimestamp(d["start_time"]) for d in index_data_list
        ]
        indices = [d["index"] for d in index_data_list]

        plt.figure(figsize=(16, 9))
        plt.plot(start_times, indices, marker="o")
        plt.xlabel("Start Time")
        plt.ylabel("Overall Traffic Index")
        plt.title("Overall Traffic Index Over Time")
        plt.grid(True)
        chart_path = os.path.join("images", "chart_overall_traffic_index.png")
        plt.savefig(chart_path)
        plt.close()
        log.info(f"Wrote {File(chart_path)}")
        return chart_path

    def get_lines_for_index(self) -> list[str]:
        lines = ["## Overall Traffic Index", ""]
        chart_path = self.build_index_chart()
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines

    def get_lines_for_routes(self) -> list[str]:
        lines = ["## Routes", ""]
        for route in self.undirected_journey_route_list:
            lines.extend([f"### {route.name}", ""])
            chart_path = route.build_chart()
            lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines

    def build_readme(self):
        lines = (
            [
                "# Colombo Traffic Index (cmb_traffic)",
                "",
            ]
            + self.get_lines_for_index()
            + self.get_lines_for_routes()
        )
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
