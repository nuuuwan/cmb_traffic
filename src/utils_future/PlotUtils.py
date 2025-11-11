import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import File, Log

from utils_future.TimeUtils import TimeUtils

log = Log("PlotUtils")


class PlotUtils:
    TIME_FORMAT = "%Y-%m-%d (%a) %H:%M"
    TIME_FORMAT_SHORT = "%Y-%m-%d"

    @staticmethod
    def write(plot_path: str):
        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter(
                PlotUtils.TIME_FORMAT_SHORT, tz=TimeUtils.LK_TZ
            )
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
        plt.tight_layout()
        plt.legend()
        plt.grid(True, alpha=0.1)
        plt.xticks()
        plt.savefig(plot_path, dpi=150)
        plt.close()

        log.info(f"Wrote {File(plot_path)}")
        return plot_path
