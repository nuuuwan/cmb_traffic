class ReadMeIndexChartUtilsMixin:

    DEFAULT_CHART_DAYS = 28

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
