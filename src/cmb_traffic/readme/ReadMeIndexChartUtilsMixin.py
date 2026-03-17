from datetime import datetime

from utils_future import TimeUtils


class ReadMeIndexChartUtilsMixin:

    DEFAULT_CHART_DAYS = 14

    def filter_to_chart_days(self, journey_d_list):
        if not journey_d_list:
            return journey_d_list
        max_ut_start = max(d["ut_start"] for d in journey_d_list)
        cutoff_ut = max_ut_start - self.DEFAULT_CHART_DAYS * 86400
        return [d for d in journey_d_list if d["ut_start"] >= cutoff_ut]

    @staticmethod
    def append_ttrs(journey_d_list):
        updated_journey_d_list = []
        max_direct_speed_kmph = max(
            [d["direct_speed_kmph"] for d in journey_d_list]
        )

        for d in journey_d_list:
            direct_speed_kmph = d["direct_speed_kmph"]
            d["ttr"] = max_direct_speed_kmph / direct_speed_kmph
            updated_journey_d_list.append(d)

        return updated_journey_d_list

    @staticmethod
    def get_period_label(journey_d_list):
        if not journey_d_list:
            return ""
        ut_starts = [d["ut_start"] for d in journey_d_list]
        min_dt = datetime.fromtimestamp(min(ut_starts), tz=TimeUtils.LK_TZ)
        max_dt = datetime.fromtimestamp(max(ut_starts), tz=TimeUtils.LK_TZ)
        return (
            f"{min_dt.strftime('%Y-%m-%d')}"
            f" to {max_dt.strftime('%Y-%m-%d')}"
        )

    @staticmethod
    def get_period_label_from_datetimes(dt_list):
        if not dt_list:
            return ""
        min_dt = min(dt_list)
        max_dt = max(dt_list)
        return (
            f"{min_dt.strftime('%Y-%m-%d')}"
            f" to {max_dt.strftime('%Y-%m-%d')}"
        )
