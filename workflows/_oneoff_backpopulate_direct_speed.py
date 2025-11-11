import os

from utils import JSONFile, LatLng, Log

log = Log("_oneoff_backpopulate_direct_speed")


def main():
    dir_root = os.path.join("data", "journeys")
    for dir_parent, __, file_names in os.walk(dir_root):
        for file_name in file_names:
            if file_name.endswith(".json"):
                file_path = os.path.join(dir_parent, file_name)
                json_file = JSONFile(file_path)
                log.debug(f"Processing {json_file}")
                d = json_file.read()
                if "direct_speed_kmph" not in d:
                    if "start_location" in d:
                        start_latlng = LatLng(
                            lat=d["start_location"]["latlng"][0],
                            lng=d["start_location"]["latlng"][1],
                        )
                        end_latlng = LatLng(
                            lat=d["end_location"]["latlng"][0],
                            lng=d["end_location"]["latlng"][1],
                        )
                    else:
                        start_latlng = LatLng(
                            lat=d["start_latlng"][0], lng=d["start_latlng"][1]
                        )
                        end_latlng = LatLng(
                            lat=d["end_latlng"][0], lng=d["end_latlng"][1]
                        )
                    direct_distance_km = start_latlng.distance(end_latlng)
                    assert direct_distance_km / d["distance_km"] < 1.1
                    d["direct_distance_km"] = direct_distance_km
                    d["direct_speed_kmph"] = direct_distance_km / (
                        d["duration_min"] / 60
                    )
                    assert d["direct_speed_kmph"] / d["avg_speed_kmph"] < 1.1
                    json_file.write(d)
                    log.info(f"Updated {json_file} with {d}")


if __name__ == "__main__":
    main()
