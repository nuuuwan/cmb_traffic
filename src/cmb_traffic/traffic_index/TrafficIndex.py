import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import contextily as ctx
import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from gig import Ent
from matplotlib.ticker import MaxNLocator
from shapely import LineString
from shapely.geometry import Point
from utils import File, Format, LatLng, Log, Time, TimeFormat

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


class TrafficIndexReadMeMixin:

    def build_route_map(self):

        plt.figure(figsize=(8, 4.5))

        ax = plt.gca()

        ent = Ent.from_id("LG-11001")
        geo = ent.geo()

        geometry = [geo for geo in geo.geometry]
        gdf = gpd.GeoDataFrame(geometry=geometry, crs=4326).to_crs(3857)
        gdf.plot(ax=ax, color=(1, 0, 0, 0.1))

        for route in self.undirected_journey_route_list:
            start = (
                route.start_latlng.lng,
                route.start_latlng.lat,
            )
            end = (
                route.end_latlng.lng,
                route.end_latlng.lat,
            )

            gdf2 = gpd.GeoDataFrame(
                geometry=[LineString([start, end])], crs=4326
            ).to_crs(3857)
            gdf2.plot(ax=ax, color="black")

            for lnglat in [start, end]:
                point_gdf = gpd.GeoDataFrame(
                    geometry=[Point(lnglat)], crs=4326
                ).to_crs(3857)
                point_gdf.plot(ax=ax, color="black", markersize=20)

        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

        ax.set_axis_off()

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        image_path = os.path.join(self.DIR_IMAGES, "map_routes.png")
        plt.savefig(image_path, dpi=300)
        log.info(f"Wrote {File(image_path)}")
        return image_path

    @staticmethod
    def append_ttrs(journey_d_list):
        n = len(journey_d_list)
        updated_journey_d_list = []
        for i in range(0, n):
            d = journey_d_list[i]
            window = []
            for j in range(i - 1, -1, -1):
                d2 = journey_d_list[j]
                if d2["start_time"] >= d["start_time"] - 3600 * 24:
                    window.append(d2)
                else:
                    break
            if not window:
                ttr = 1.0
            else:
                speeds = [d2["avg_speed_kmph"] for d2 in window]
                min_avg_speed_kmph = min(speeds)
                max_avg_speed_kmph = max(speeds)
                ttr = max_avg_speed_kmph / min_avg_speed_kmph
            d["ttr"] = ttr
            updated_journey_d_list.append(d)
        return updated_journey_d_list

    def build_ttr_chart(self):
        journey_d_list = self.append_ttrs(self.get_journey_data_list())
        start_times = [
            datetime.fromtimestamp(d["start_time"], tz=LK_TZ)
            for d in journey_d_list
        ]
        ttr_values = [d["ttr"] for d in journey_d_list]
        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, ttr_values, marker="o")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))

        plt.xlabel("Start Time")
        plt.ylabel("Travel Time Ratio (TTR)")
        plt.title("Travel Time Ratio (TTR) Over Time")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_ttr_traffic_index.png"
        )
        plt.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close()
        log.info(f"Wrote {File(chart_path)}")
        return chart_path

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

        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        chart_path = os.path.join(
            self.DIR_IMAGES, "chart_overall_traffic_index.png"
        )
        plt.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close()
        log.info(f"Wrote {File(chart_path)}")
        return chart_path

    def get_lines_for_index(self) -> list[str]:
        lines = ["## Overall Traffic Index", ""]
        chart_path = self.build_index_chart()
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        ttr_chart_path = self.build_ttr_chart()
        lines.extend([f"![{ttr_chart_path}]({ttr_chart_path})", ""])
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
        return lines

    def build_readme(self):
        journey_d_list = self.get_journey_data_list()
        if not journey_d_list:
            log.warning("No journey data found; skipping README generation")
            return
        time_updated = max([d["start_time"] for d in journey_d_list])
        time_updated_for_badge = Format.badge(
            TimeFormat.TIME.format(Time(time_updated))
        )
        lines = (
            [
                "# 🇱🇰 Colombo Traffic Index (cmb_traffic)",
                "",
                "![LatestEstimateFor](https://img.shields.io/badge"
                + f"/latest_estimate_for-{time_updated_for_badge}-green)",
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


@dataclass
class TrafficIndex(TrafficIndexReadMeMixin):
    undirected_journey_route_list: list[JourneyRoute]
    DIR_IMAGES = JourneyRoute.DIR_IMAGES

    README_PATH = "README.md"

    @staticmethod
    def standard_route():
        bambalapitiya = LatLng(6.895572468746244, 79.85483770889027)
        borella = LatLng(6.910882574522934, 79.88789773709671)
        dematagoda = LatLng(6.943175860321491, 79.87820817923517)
        fort = LatLng(6.931424355241801, 79.84220762949998)
        mattakkuliya = LatLng(6.980026983331188, 79.87551282104877)
        pamankada = LatLng(6.871812810816128, 79.88456400975986)
        wellawatte = LatLng(6.863288956321618, 79.86360827087549)
        return TrafficIndex(
            TrafficIndex.build_route_list(
                dict(
                    dematagoda=dematagoda,
                    fort=fort,
                    mattakkuliya=mattakkuliya,
                ),
            )
            + TrafficIndex.build_route_list(
                dict(
                    bambalapitiya=bambalapitiya,
                    borella=borella,
                    dematagoda=dematagoda,
                    fort=fort,
                ),
            )
            + TrafficIndex.build_route_list(
                dict(
                    bambalapitiya=bambalapitiya,
                    borella=borella,
                    pamankada=pamankada,
                    wellawatte=wellawatte,
                ),
            ),
        )

    @staticmethod
    def build_route_list(
        base_location_idx: dict[str, LatLng],
    ) -> "TrafficIndex":
        undirected_journey_route_list = []
        n = len(base_location_idx)
        location_names = list(base_location_idx.keys())
        for i in range(n - 1):
            for j in range(i + 1, n):
                start_name = location_names[i]
                end_name = location_names[j]
                route = JourneyRoute(
                    name=f"{start_name.title()} to {end_name.title()}",
                    start_latlng=base_location_idx[start_name],
                    end_latlng=base_location_idx[end_name],
                )
                undirected_journey_route_list.append(route)
        return undirected_journey_route_list

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
                dict(
                    start_time=start_time, n=n, avg_speed_kmph=avg_speed_kmph
                )
            )
        overall_d_list.sort(key=lambda d: d["start_time"])
        return overall_d_list
