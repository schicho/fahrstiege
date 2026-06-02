import json
from datetime import date

STATIONS_TO_TRACK = ["Karlsplatz"]

def load_current_broken_stations() -> list[str]:
    with open("data/wl-current.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    broken_stations = set()
    for station in data["data"]["trafficInfos"]:
        station_name = station["title"]
        broken_stations.add(station_name)
    return broken_stations

def update_counter(broken_stations: set[str]) -> dict[str, int]:
    with open("data/counter.json", "r", encoding="utf-8") as f:
        counters = json.load(f)
    for station in STATIONS_TO_TRACK:
        if station not in counters or station in broken_stations:
            # initialize count for the station if it is not in the counter or reset if it is currently broken
            counters[station] = {"count": 0}
        elif counters[station]["last_updated"] != date.today().isoformat() and station not in broken_stations:
            # only increment count if the station is not broken and the date has changed (i.e. it is the next day)
            counters[station]["count"] += 1

        counters[station]["last_updated"] = date.today().isoformat()
        
    return counters

if __name__ == "__main__":
    current_broken_stations = load_current_broken_stations()
    counter = update_counter(current_broken_stations)

    with open("data/counter.json", "w", encoding="utf-8") as f:
        json.dump(counter, f, ensure_ascii=False, indent=4)