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

    def build_route_map(self):
        ax = plt.gca()

        def add_geometry(geometry, color):
            gpd.GeoDataFrame(geometry=geometry, crs=4326).to_crs(3857).plot(
                ax=ax, color=color, figsize=(8, 4.5)
            )

        add_geometry(
            [geo for geo in Ent.from_id("LG-11001").geo().geometry],
            color=(1, 0, 0, 0.1),
        )

        for route in self.undirected_journey_route_list:
            start = (
                route.start_latlng.lng,
                route.start_latlng.lat,
            )
            end = (
                route.end_latlng.lng,
                route.end_latlng.lat,
            )
            add_geometry([LineString([start, end])], color="black")
            for lnglat in [start, end]:
                add_geometry([Point(lnglat)], color="black")

        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_axis_off()
        os.makedirs(self.DIR_IMAGES, exist_ok=True)
        image_path = os.path.join(self.DIR_IMAGES, "map_routes.png")
        plt.savefig(image_path, dpi=300)
        log.info(f"Wrote {File(image_path)}")
        return image_path

    def get_lines_for_route(self, route) -> list[str]:
        lines = []
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

    def get_lines_for_routes(self) -> list[str]:
        lines = ["## Routes", ""]
        route_image_path = self.build_route_map()
        lines.extend([f"![{route_image_path}]({route_image_path})", ""])
        for route in self.undirected_journey_route_list:
            lines.extend(self.get_lines_for_route(route))
        return lines
