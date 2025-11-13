import os

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
from gig import Ent
from shapely import LineString
from shapely.geometry import Point
from utils import File, Log

log = Log("ReadMe")


class ReadMeRoutesMixin:

    def get_location_list(self) -> list[str]:
        location_set = set()
        for route in self.traffic_index.undirected_route_list:
            location_set.add(route.start_location)
            location_set.add(route.end_location)
        location_list = list(location_set)
        location_list.sort(key=lambda loc: loc.latlng.lat, reverse=True)
        return location_list

    @staticmethod
    def __get_gdf__(geometry):
        return gpd.GeoDataFrame(geometry=geometry, crs=4326).to_crs(3857)

    @staticmethod
    def __add_geometry__(geometry, color):
        ax = plt.gca()
        ReadMeRoutesMixin.__get_gdf__(geometry).plot(
            ax=ax, color=color, figsize=(8, 4.5)
        )

    def __draw_paths__(self):
        name_to_lnglat = {}
        ax = plt.gca()
        for i_route, route in enumerate(
            self.traffic_index.undirected_route_list, start=1
        ):
            start = route.start_location.lnglat
            end = route.end_location.lnglat
            name_to_lnglat[route.start_location.name] = start
            name_to_lnglat[route.end_location.name] = end
            self.__add_geometry__([LineString([start, end])], color="black")

            start_point_gdf = ReadMeRoutesMixin.__get_gdf__([Point(start)])
            end_point_gdf = ReadMeRoutesMixin.__get_gdf__([Point(end)])
            x_start, y_start = (
                start_point_gdf.geometry.iloc[0].x,
                start_point_gdf.geometry.iloc[0].y,
            )
            x_end, y_end = (
                end_point_gdf.geometry.iloc[0].x,
                end_point_gdf.geometry.iloc[0].y,
            )
            p = 0.6
            q = 1 - p
            x_mid, y_mid = (p * x_start + q * x_end), (
                p * y_start + q * y_end
            )
            ax.text(
                x_mid,
                y_mid,
                f"R{i_route:02d}",
                fontsize=4,
                color="white",
                ha="center",
                va="center",
                rotation=0,
                bbox=dict(
                    boxstyle="round,pad=0.4",
                    facecolor="black",
                ),
            )

        return name_to_lnglat

    def __draw_points__(self, location_list, name_to_lnglat):
        ax = plt.gca()
        for i_location, location in enumerate(location_list, start=1):
            lnglat = name_to_lnglat[location.name]

            self.__add_geometry__([Point(lnglat)], color="black")

            point_gdf = ReadMeRoutesMixin.__get_gdf__([Point(lnglat)])
            x, y = point_gdf.geometry.iloc[0].x, point_gdf.geometry.iloc[0].y

            ax.text(
                x,
                y,
                f"{i_location}. {location.name}",
                fontsize=4,
                color="black",
                ha="center",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.4",
                    facecolor="white",
                ),
            )

    def build_route_map(self, location_list):
        ax = plt.gca()
        self.__add_geometry__(
            [geo for geo in Ent.from_id("LG-11001").geo().geometry],
            color=(0, 0.5, 1, 0.3),
        )

        name_to_lnglat = self.__draw_paths__()
        self.__draw_points__(location_list, name_to_lnglat)

        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_axis_off()
        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        image_path = os.path.join(self.DIR_IMAGES, "map_routes.png")
        plt.savefig(image_path, dpi=300, bbox_inches="tight")
        log.info(f"Wrote {File(image_path)}")
        return image_path

    def get_lines_for_route(self, i_route, route) -> list[str]:
        lines = []
        lines.extend(
            [
                f"#### R{
                    i_route:02d}. [{
                    route.name_bidirectional}]({
                    route.url})",
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
        location_list = self.get_location_list()
        for i_location, location in enumerate(location_list, start=1):
            lines.append(
                f"{i_location}. "
                + f"[{location.name}]({location.url()}):"
                + f" {location.details}"
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
        route_image_path = self.build_route_map(location_list)
        lines.extend(
            [
                f"![Route Map]({route_image_path})",
                "",
            ]
        )

        lines.extend(
            [
                "### Direct Speed by Route",
                "",
            ]
        )
        for i_route, route in enumerate(
            self.traffic_index.undirected_route_list, start=1
        ):
            lines.extend(self.get_lines_for_route(i_route, route))
        return lines
