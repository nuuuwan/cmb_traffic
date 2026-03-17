class ReadMeIndexChartUtilsMixin:
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
