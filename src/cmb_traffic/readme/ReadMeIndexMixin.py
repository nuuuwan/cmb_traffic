from cmb_traffic.readme.ReadMeIndexChart7DaySpeedMixin import \
    ReadMeIndexChart7DaySpeedMixin
from cmb_traffic.readme.ReadMeIndexChartDirectSpeedMixin import \
    ReadMeIndexChartDirectSpeedMixin
from cmb_traffic.readme.ReadMeIndexChartSpeedByDayOfWeekMixin import \
    ReadMeIndexChartSpeedByDayOfWeekMixin
from cmb_traffic.readme.ReadMeIndexChartTTRByTimeOfDayMixin import \
    ReadMeIndexChartTTRByTimeOfDayMixin
from cmb_traffic.readme.ReadMeIndexChartTTRMixin import \
    ReadMeIndexChartTTRMixin


class ReadMeIndexMixin(
    ReadMeIndexChartTTRMixin,
    ReadMeIndexChartDirectSpeedMixin,
    ReadMeIndexChartTTRByTimeOfDayMixin,
    ReadMeIndexChartSpeedByDayOfWeekMixin,
    ReadMeIndexChart7DaySpeedMixin,
):
    def get_lines_for_cti(self, journey_d_list) -> list[str]:
        lines = []

        ttr_chart_path, current_ttr_value = self.build_ttr_chart(
            journey_d_list
        )
        lines.extend(
            [
                f"## Colombo Traffic Index (CTI) = {current_ttr_value:.2f}x",
                "",
            ]
        )

        lines.extend([f"![{ttr_chart_path}]({ttr_chart_path})", ""])

        lines.extend(["### Average CTI by Time of Day", ""])
        ttr_by_hour_path = self.build_ttr_by_time_of_day_chart(journey_d_list)
        if ttr_by_hour_path:
            lines.extend([f"![{ttr_by_hour_path}]({ttr_by_hour_path})", ""])

        lines.extend(["### Average Speed by Day of Week", ""])
        speed_by_dow_path = self.build_speed_by_day_of_week_chart(
            journey_d_list
        )
        if speed_by_dow_path:
            lines.extend([f"![{speed_by_dow_path}]({speed_by_dow_path})", ""])

        lines.extend(["### Overall Direct Speed (ODS)", ""])
        chart_path = self.build_direct_speed_chart(journey_d_list)
        lines.extend([f"![{chart_path}]({chart_path})", ""])

        lines.extend(["### 7-Day Moving Avg Speed (full history)", ""])
        speed_chart_path = self.build_7day_speed_chart(journey_d_list)
        if speed_chart_path:
            lines.extend([f"![{speed_chart_path}]({speed_chart_path})", ""])
        return lines
