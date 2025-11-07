from utils import LatLng, Log

from cmb_traffic import JourneyRoute, TrafficIndex

log = Log("pipeline")


def main():
    traffic_index = TrafficIndex(
        [
            JourneyRoute(
                "Fort to Wellawatte",
                LatLng(6.931424355241801, 79.84220762949998),
                LatLng(6.863288956321618, 79.86360827087549),
            ),
            JourneyRoute(
                "Kolpetty to Borella",
                LatLng(6.911641573257379, 79.84959789405549),
                LatLng(6.909536122722376, 79.88866478656242),
            ),
            JourneyRoute(
                "Peliyagoda to Pamankada",
                LatLng(6.9542078305459345, 79.88192542814637),
                LatLng(6.878312139239246, 79.87634010744225),
            ),
        ]
    )
    traffic_index.write_all()
    traffic_index.build_readme()


if __name__ == "__main__":
    main()
