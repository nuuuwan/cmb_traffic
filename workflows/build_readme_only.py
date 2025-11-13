from cmb_traffic import ReadMe, TrafficIndex


def main():
    traffic_index = TrafficIndex.standard_route()
    ReadMe(traffic_index).build_readme()


if __name__ == "__main__":
    main()
