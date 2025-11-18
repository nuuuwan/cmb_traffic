from cmb_traffic import ReadMe, TrafficIndex


def main():
    for traffic_index in TrafficIndex.all():
        ReadMe(traffic_index).build_readme()


if __name__ == "__main__":
    main()
