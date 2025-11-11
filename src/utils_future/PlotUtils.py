import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from utils import File, Log

from utils_future.TimeUtils import TimeUtils

log = Log("PlotUtils")


class PlotUtils:
    TIME_FORMAT = "%I:%M%p (%a, %Y-%m-%d)"
    TIME_FORMAT_SHORT = "%Y-%m-%d"

    @staticmethod
    def write(plot_path: str):
        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                PlotUtils.TIME_FORMAT_SHORT, tz=TimeUtils.LK_TZ
            )
        )
        ax.xaxis.set_major_locator(mdates.DayLocator(tz=TimeUtils.LK_TZ))
        plt.tight_layout()
        plt.legend()
        plt.grid(True, alpha=0.1)
        plt.xticks()
        plt.savefig(plot_path, dpi=150)
        plt.close()

        log.info(f"Wrote {File(plot_path)}")
        return plot_path
