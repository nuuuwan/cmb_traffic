from utils import LatLng, Log

from cmb_traffic import JourneyRoute, TrafficIndex

log = Log("pipeline")


def main():
    fort = LatLng(6.931424355241801, 79.84220762949998)
    wellawatte = LatLng(6.863288956321618, 79.86360827087549)
    kolpetty = LatLng(6.911641573257379, 79.84959789405549)
    borella = LatLng(6.909536122722376, 79.88866478656242)
    peliyagoda = LatLng(6.9542078305459345, 79.88192542814637)
    pamankada = LatLng(6.878312139239246, 79.87634010744225)
    town_hall = LatLng(6.917289879635986, 79.8647742082981)
    havelock_town = LatLng(6.881700759766507, 79.86974762755251)

    traffic_index = TrafficIndex(
        [
            # North-South
            JourneyRoute("Fort to Wellawatte", fort, wellawatte),
            JourneyRoute(
                "Town-Hall to Havelock-Town", town_hall, havelock_town
            ),
            JourneyRoute("Peliyagoda to Pamankada", peliyagoda, pamankada),
            # West-East
            JourneyRoute("Fort to Peliyagoda", fort, peliyagoda),
            JourneyRoute("Kolpetty to Borella", kolpetty, borella),
            JourneyRoute("Wellawatte to Pamankada", wellawatte, pamankada),
        ]
    )
    # traffic_index.write_all()
    traffic_index.build_readme()


if __name__ == "__main__":
    main()
