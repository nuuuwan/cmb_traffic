import os
from dataclasses import asdict

from utils import JSONFile, Log

from cmb_traffic import Journey, Location, Route

log = Log("_oneoff_backpopulate")


def main():
    dir_root = os.path.join("data", "journeys")
    for dir_parent, __, file_names in os.walk(dir_root):
        for file_name in file_names:
            if not file_name.endswith(".json"):
                continue
            file_path = os.path.join(dir_parent, file_name)
            json_file = JSONFile(file_path)
            d = json_file.read()

            has_updated = False
            if "name" in d:
                has_updated = True
                route_name = d["name"]
                start_location_name, end_location_name = route_name.split(
                    " to "
                )
                start_location = Location.from_name(start_location_name)
                end_location = Location.from_name(end_location_name)
                route = Route(
                    start_location=start_location,
                    end_location=end_location,
                )
                d["route"] = asdict(route)

                del d["name"]
                if "start_latlng" in d:
                    del d["start_latlng"]
                if "end_latlng" in d:
                    del d["end_latlng"]
                if "start_location" in d:
                    del d["start_location"]
                if "end_location" in d:
                    del d["end_location"]

            if "ut_start" in d:
                has_updated = True
                d["ut_start"] = d["ut_start"]
                del d["ut_start"]

            if has_updated:
                json_file.write(d)
                log.warning(f"Updated {json_file}")

            journey = Journey.from_file_path(file_path)
            journey.write()


if __name__ == "__main__":
    main()
