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
        if station not in station_counters:
            # initalize count object if not present
            station_counters[station] = {
                "count": 0,
                "highscore": 0,
                "last_updated": CURRENT_DATE.isoformat(),
            }
            continue

        station_counter_entry = station_counters[station]

        current_highscore = station_counter_entry["highscore"]
        current_count = station_counter_entry["count"]
        last_updated = station_counter_entry["last_updated"]

        if station in broken_stations:
            # reset if it is currently broken
            station_counter_entry["count"] = 0
            print(f"Station '{station}' is currently broken. Count reset to 0.")

        elif last_updated < CURRENT_DATE.isoformat() and station not in broken_stations:
            # only increment count if the station is not broken and the date has changed (i.e. it is the next day)
            current_count += CURRENT_DATE.day - datetime.fromisoformat(last_updated).day
            station_counter_entry["highscore"] = max(current_highscore, current_count)
            station_counter_entry["count"] = current_count
            print(
                f"Station '{station}' is not broken. Count incremented to {current_count}."
            )

        station_counter_entry["last_updated"] = CURRENT_DATE.isoformat()
        station_counters[station] = station_counter_entry

    return station_counters


if __name__ == "__main__":
    current_broken_stations = load_current_broken_stations()
    counter = update_counter(current_broken_stations)

    with open("data/counter.json", "w", encoding="utf-8") as f:
        json.dump(counter, f, ensure_ascii=False, indent=2)
