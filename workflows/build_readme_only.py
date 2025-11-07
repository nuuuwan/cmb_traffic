
from cmb_traffic import TrafficIndex


def main():
    traffic_index = TrafficIndex.standard_route()
    traffic_index.build_readme()


if __name__ == "__main__":
    main()
