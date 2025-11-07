import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import File, Format, Log, Time, TimeFormat

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


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
            datetime.fromtimestamp(d["start_time"], tz=LK_TZ)
            for d in index_data_list
        ]
        indices = [d["index"] for d in index_data_list]

        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, indices, marker="o")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Start Time")
        plt.ylabel("Overall Traffic Index")
        plt.title("Overall Traffic Index Over Time")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_path = os.path.join("images", "chart_overall_traffic_index.png")
        plt.savefig(chart_path, dpi=150, bbox_inches="tight")
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

    def get_lines_for_background(self) -> list[str]:
        lines = [
            "## 📊 About This Index",
            "",
            "The Colombo Traffic Index (CTI) provides a real-time measure of "
            "traffic congestion across key routes in Colombo. By tracking "
            "journey times throughout the day and comparing them to baseline "
            "(free-flow) conditions, this index helps:",
            "",
            "- 🚗 **Commuters** plan their travel times and avoid peak "
            "congestion",
            "- 📈 **Researchers** analyze traffic patterns and urban mobility "
            "trends",
            "- 🏛️ **Policy makers** make data-driven decisions on "
            "infrastructure and traffic management",
            "",
            "### Methodology",
            "",
            "We monitor a set of representative routes across Colombo City, "
            "measuring travel times at regular intervals throughout the day. "
            "The traffic index for each route is calculated as:",
            "",
            "```python",
            "Index = Current Travel Time / Minimum Observed Travel Time",
            "```",
            "",
            "An index of 1.0 indicates free-flow conditions, while higher "
            "values indicate congestion. For example, an index of 2.0 means "
            "travel takes twice as long as under ideal conditions.",
            "",
        ]
        return lines

    def build_readme(self):
        time_updated_for_badge = Format.badge(
            TimeFormat.TIME.format(Time.now())
        )
        lines = (
            [
                "# Colombo Traffic Index (cmb_traffic)",
                "",
                "![LastUpdated](https://img.shields.io/badge"
                + f"/last_updated-{time_updated_for_badge}-green)",
                "",
            ]
            + self.get_lines_for_background()
            + self.get_lines_for_index()
            + self.get_lines_for_routes()
        )
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
