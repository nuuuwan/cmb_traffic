import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from staticmap import CircleMarker, Line, StaticMap
from utils import File, Format, LatLng, Log, Time, TimeFormat

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


@dataclass
class TrafficIndex:
    undirected_journey_route_list: list[JourneyRoute]

    README_PATH = "README.md"

    @staticmethod
    def standard_route():
        fort = LatLng(6.931424355241801, 79.84220762949998)
        wellawatte = LatLng(6.863288956321618, 79.86360827087549)
        kolpetty = LatLng(6.911641573257379, 79.84959789405549)
        borella = LatLng(6.909536122722376, 79.88866478656242)
        peliyagoda = LatLng(6.9542078305459345, 79.88192542814637)
        pamankada = LatLng(6.878312139239246, 79.87634010744225)
        maradana = LatLng(6.928434938665055, 79.86434731553278)
        havelock_town = LatLng(6.881700759766507, 79.86974762755251)

        return TrafficIndex(
            [
                # North-South
                JourneyRoute("Fort to Wellawatte", fort, wellawatte),
                JourneyRoute(
                    "Maradana to Havelock-Town", maradana, havelock_town
                ),
                JourneyRoute("Peliyagoda to Pamankada", peliyagoda, pamankada),
                # West-East
                JourneyRoute("Fort to Peliyagoda", fort, peliyagoda),
                JourneyRoute("Kolpetty to Borella", kolpetty, borella),
                JourneyRoute("Wellawatte to Pamankada", wellawatte, pamankada),
            ]
        )

    def get_full_journey_route_list(self) -> list[JourneyRoute]:
        return self.undirected_journey_route_list + [
            route.reverse() for route in self.undirected_journey_route_list
        ]

    def write_all(self):
        for route in self.get_full_journey_route_list():
            journey = Journey.from_route_now(route)
            journey.write_journey_info()

    def get_journey_data_list(self):
        start_time_to_d_list = {}
        for route in self.get_full_journey_route_list():
            d_list = route.get_journey_data_list()
            for d in d_list:
                start_time = d["start_time"]
                if start_time not in start_time_to_d_list:
                    start_time_to_d_list[start_time] = []
                start_time_to_d_list[start_time].append(d["avg_speed_kmph"])

        overall_d_list = []
        for start_time, speed_list in start_time_to_d_list.items():
            n = len(speed_list)
            avg_speed_kmph = sum(speed_list) / n
            overall_d_list.append(
                dict(start_time=start_time, n=n, avg_speed_kmph=avg_speed_kmph)
            )
        overall_d_list.sort(key=lambda d: d["start_time"])
        return overall_d_list

    def build_route_map(self):
        m = StaticMap(800, 800)

        for route in self.undirected_journey_route_list:

            start = (
                route.start_latlng.lng,
                route.start_latlng.lat,
            )
            end = (
                route.end_latlng.lng,
                route.end_latlng.lat,
            )
            m.add_line(Line([start, end], "black", 3))
            m.add_marker(CircleMarker(start, "red", 8))
            m.add_marker(CircleMarker(end, "red", 10))

        image = m.render()
        image_path = os.path.join("images", "map_routes.png")
        image.save(image_path)
        log.info(f"Wrote {File(image_path)}")
        return image_path

    def build_index_chart(self):
        journey_d_list = self.get_journey_data_list()
        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=LK_TZ)
            for d in journey_d_list
        ]
        avg_speed_kmphs = [d["avg_speed_kmph"] for d in journey_d_list]

        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, avg_speed_kmphs, marker="o")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Start Time")
        plt.ylabel("Average Speed (km/h)")
        plt.title("Average Speed Over Time")
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
        route_image_path = self.build_route_map()
        lines.extend([f"![{route_image_path}]({route_image_path})", ""])
        for route in self.undirected_journey_route_list:
            route_title = route.name.replace(" to ", " ↔ ")
            lines.extend(
                [
                    f"### {route_title}",
                    "",
                    f"📍 [{route.start_latlng} to {route.end_latlng}]"
                    + f"({route.url})",
                    "",
                ]
            )
            chart_path = route.build_chart()
            lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines

    def get_lines_for_background(self) -> list[str]:
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
            "### Methodology",
            "",
            "We monitor a set of representative routes across Colombo City, "
            "measuring travel times and speeds at regular intervals "
            "throughout the day. Each route is monitored in both directions "
            "to capture bidirectional traffic patterns. The overall traffic "
            "condition is assessed by calculating the average speed across "
            "all monitored routes at each time point.",
            "",
            "Lower average speeds indicate heavier traffic congestion, "
            "while higher speeds suggest free-flow conditions. By tracking "
            "these patterns over time, we can identify peak congestion "
            "periods and seasonal trends.",
            "",
        ]
        return lines

    def build_readme(self):
        time_updated_for_badge = Format.badge(
            TimeFormat.TIME.format(Time.now())
        )
        lines = (
            [
                "# 🇱🇰 Colombo Traffic Index (cmb_traffic)",
                "",
                "![LastUpdated](https://img.shields.io/badge"
                + f"/last_updated-{time_updated_for_badge}-green)",
                "",
            ]
            + self.get_lines_for_background()
            + self.get_lines_for_index()
            + self.get_lines_for_routes()
            + [
                "![Maintainer]"
                + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
                "![MadeWith]"
                + "(https://img.shields.io/badge/made_with-python-blue)",
                "[![License: MIT]"
                + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
                + "(https://opensource.org/licenses/MIT)",
                "",
            ]
        )
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
