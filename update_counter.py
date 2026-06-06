import json
from datetime import datetime
from zoneinfo import ZoneInfo

STATIONS_TO_TRACK = ["Karlsplatz"]
CURRENT_DATE = datetime.now(ZoneInfo("Europe/Vienna")).date()

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
        station_counters = json.load(f)
    for station in STATIONS_TO_TRACK:
        if station not in station_counters or station in broken_stations:
            # initialize count for the station if it is not in the counter or reset if it is currently broken
            station_counters[station] = {"count": 0}
            print(f"Station '{station}' is currently broken. Count reset to 0.")
        elif station_counters[station]["last_updated"] < CURRENT_DATE.isoformat() and station not in broken_stations:
            # only increment count if the station is not broken and the date has changed (i.e. it is the next day)
            print(CURRENT_DATE.day - datetime.fromisoformat(station_counters[station]["last_updated"]).day)
            station_counters[station]["count"] += CURRENT_DATE.day - datetime.fromisoformat(station_counters[station]["last_updated"]).day
            print(f"Station '{station}' is not broken. Count incremented to {station_counters[station]['count']}.")

        station_counters[station]["last_updated"] = CURRENT_DATE.isoformat()
        
    return station_counters

if __name__ == "__main__":
    current_broken_stations = load_current_broken_stations()
    counter = update_counter(current_broken_stations)

    with open("data/counter.json", "w", encoding="utf-8") as f:
        json.dump(counter, f, ensure_ascii=False, indent=4)