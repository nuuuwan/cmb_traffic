import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import File, Log

from utils_future.TimeUtils import TimeUtils

log = Log("PlotUtils")


class PlotUtils:
    @staticmethod
    def write(plot_path: str):
        ax = plt.gca()
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d %H:%M", tz=TimeUtils.LK_TZ)
        )
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))
        plt.legend()
        plt.grid(True, alpha=0.1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(plot_path, dpi=150)
        plt.close()
        log.info(f"Wrote {File(plot_path)}")
        return plot_path
