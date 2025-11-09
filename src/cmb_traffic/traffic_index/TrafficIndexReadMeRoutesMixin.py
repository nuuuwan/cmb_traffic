import os

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
from gig import Ent
from shapely import LineString
from shapely.geometry import Point
from utils import File, Log

log = Log("TrafficIndexReadMeRoutesMixin")


class TrafficIndexReadMeRoutesMixin:

    def get_location_list(self) -> list[str]:
        location_set = set()
        for route in self.undirected_journey_route_list:
            location_set.add(route.start_location)
            location_set.add(route.end_location)
        location_list = list(location_set)
        location_list.sort()
        return location_list

    @staticmethod
    def __add_geometry__(geometry, color):
        ax = plt.gca()
        gpd.GeoDataFrame(geometry=geometry, crs=4326).to_crs(3857).plot(
            ax=ax, color=color, figsize=(8, 4.5)
        )

    def __draw_paths__(self):
        name_to_lnglat = {}
        for route in self.undirected_journey_route_list:
            start = route.start_location.lnglat
            end = route.end_location.lnglat
            name_to_lnglat[route.start_location.name] = start
            name_to_lnglat[route.end_location.name] = end
            self.__add_geometry__([LineString([start, end])], color="black")

        return name_to_lnglat

    def __draw_points__(self, name_to_lnglat):
        ax = plt.gca()
        for name, lnglat in name_to_lnglat.items():
            self.__add_geometry__([Point(lnglat)], color="black")

            point_gdf = gpd.GeoDataFrame(
                geometry=[Point(lnglat)], crs=4326
            ).to_crs(3857)
            x, y = point_gdf.geometry.iloc[0].x, point_gdf.geometry.iloc[0].y

            ax.text(
                x,
                y,
                name,
                fontsize=4,
                ha="center",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    facecolor="white",
                ),
            )

    def build_route_map(self):
        ax = plt.gca()
        self.__add_geometry__(
            [geo for geo in Ent.from_id("LG-11001").geo().geometry],
            color=(1, 0, 0, 0.1),
        )

        name_to_lnglat = self.__draw_paths__()
        self.__draw_points__(name_to_lnglat)

        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_axis_off()
        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        image_path = os.path.join(self.DIR_IMAGES, "map_routes.png")
        plt.savefig(image_path, dpi=300, bbox_inches="tight")
        log.info(f"Wrote {File(image_path)}")
        return image_path

    def get_lines_for_route(self, route) -> list[str]:
        lines = []
        lines.extend(
            [
                f"### [{route.name_bidirectional}]({route.url})",
                "",
            ]
        )
        chart_path = route.build_chart()
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines

    def get_lines_for_routes(self) -> list[str]:
        lines = [
            "## Routes",
            "",
            "The Traffic Index monitors travel times and speeds across a "
            "carefully selected set of routes representing key traffic "
            "corridors in Colombo. Each route is tracked in both "
            "directions to provide a comprehensive view of traffic "
            "conditions throughout the day.",
            "",
            "The current version uses routes between the following locations:",
            "",
        ]
        for location in self.get_location_list():
            lines.append(
                f"- [{location.name}]({location.url()}): {location.details}"
            )
        lines.extend(
            [
                "",
                "### Route Map",
                "",
                "The map below shows all monitored routes connecting these "
                "locations:",
                "",
            ]
        )
        route_image_path = self.build_route_map()

        lines.extend(
            [
                f"![Route Map]({route_image_path})",
                "",
            ]
        )
        for route in self.undirected_journey_route_list:
            lines.extend(self.get_lines_for_route(route))
        return lines
