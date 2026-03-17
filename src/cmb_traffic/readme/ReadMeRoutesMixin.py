from cmb_traffic.readme.ReadMeRoutesChartDirectSpeedMixin import \
    ReadMeRoutesChartDirectSpeedMixin
from cmb_traffic.readme.ReadMeRoutesChartMapMixin import \
    ReadMeRoutesChartMapMixin


class ReadMeRoutesMixin(
    ReadMeRoutesChartDirectSpeedMixin,
    ReadMeRoutesChartMapMixin,
):

    def get_location_list(self) -> list[str]:
        location_set = set()
        for route in self.traffic_index.undirected_route_list:
            location_set.add(route.start_location)
            location_set.add(route.end_location)
        location_list = list(location_set)
        location_list.sort(key=lambda loc: loc.latlng.lat, reverse=True)
        return location_list

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
        chart_path = self.build_chart_for_route(route)
        lines.extend([f"![{chart_path}]({chart_path})", ""])
        return lines

    def get_lines_for_routes(self) -> list[str]:
        lines = [
            "## Routes",
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
