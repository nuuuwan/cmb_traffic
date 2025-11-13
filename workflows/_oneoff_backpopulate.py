import os
from dataclasses import asdict

from utils import JSONFile, Log, Time, TimeFormat

from cmb_traffic import Location, Route

log = Log("_oneoff_backpopulate")


def main():
    dir_root = os.path.join("data", "journeys")
    for dir_parent, __, file_names in os.walk(dir_root):
        for file_name in file_names:
            if not file_name.endswith(".json"):
                continue
            file_path = os.path.join(dir_parent, file_name)
            json_file = JSONFile(file_path)
            log.debug(f"Processing {json_file}")
            d = json_file.read()

            if "name" in d:
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

            if "start_time" in d:
                d["ut_start"] = d["start_time"]
                del d["start_time"]

            json_file.write(d)


if __name__ == "__main__":
    main()
