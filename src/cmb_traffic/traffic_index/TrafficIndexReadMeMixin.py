import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import File, Format, Log, Time, TimeFormat

from cmb_traffic.traffic_index.TrafficIndexReadMeRoutesMixin import \
    TrafficIndexReadMeRoutesMixin
from utils_future import TimeUtils

log = Log("TrafficIndexReadMeMixin")


class TrafficIndexReadMeMixin(TrafficIndexReadMeRoutesMixin):

    def get_time_updated_for_badge(self) -> str:
        journey_d_list = self.get_journey_data_list()
        time_updated = max([d["start_time"] for d in journey_d_list])
        time_updated_for_badge = Format.badge(
            TimeFormat.TIME.format(Time(time_updated))
        )
        return time_updated_for_badge

    def get_lines_for_header(self) -> list[str]:
        time_updated_for_badge = self.get_time_updated_for_badge()
        return [
            "# 🇱🇰 Colombo Traffic Index (cmb_traffic)",
            "",
            "![LatestEstimateFor](https://img.shields.io/badge"
            + f"/latest_estimate_for-{time_updated_for_badge}-green)",
            "",
        ]

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
            datetime.fromtimestamp(d["start_time"], tz=TimeUtils.LK_TZ)
            for d in journey_d_list
        ]
        ttr_values = [d["ttr"] for d in journey_d_list]
        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, ttr_values, marker="o")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=TimeUtils.LK_TZ)
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
            datetime.fromtimestamp(d["start_time"], tz=TimeUtils.LK_TZ)
            for d in journey_d_list
        ]
        avg_speed_kmphs = [d["avg_speed_kmph"] for d in journey_d_list]

        plt.figure(figsize=(8, 4.5))
        plt.plot(start_times, avg_speed_kmphs, marker="o")

        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=TimeUtils.LK_TZ)
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

    def get_lines_for_ttr(self) -> list[str]:
        return [
            "### Travel Time Ratio (TTR)",
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

    def get_lines_for_methodology(self) -> list[str]:
        return [
            "### Methodology",
            "",
            "We monitor a set of representative routes across Colombo City, "
            "measuring travel times and speeds at regular intervals "
            "throughout the day. Each route is monitored in both directions "
            "to capture bidirectional traffic patterns. The overall traffic "
            "condition is assessed by calculating the average speed across "
            "all monitored routes at each time point.",
            "",
        ]

    def get_lines_for_about(self) -> list[str]:
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
        ]
        return lines

    def get_lines_for_footer(self) -> list[str]:
        return [
            "![Maintainer]"
            + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
            "![MadeWith]"
            + "(https://img.shields.io/badge/made_with-python-blue)",
            "[![License: MIT]"
            + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
            + "(https://opensource.org/licenses/MIT)",
            "",
        ]

    def build_readme(self):

        lines = (
            self.get_lines_for_header()
            + self.get_lines_for_about()
            + self.get_lines_for_methodology()
            + self.get_lines_for_ttr()
            + self.get_lines_for_index()
            + self.get_lines_for_routes()
            + self.get_lines_for_footer()
        )
        readme_file = File(self.README_PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
