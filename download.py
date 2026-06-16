import json
from urllib import error, request

URL = "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?name=fahrtreppeninfo"
USER_AGENT = "schicho/fahrstiege (https://github.com/schicho/fahrstiege)"


def download_data(timeout=10):
    req = request.Request(URL, headers={"User-Agent": USER_AGENT})
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            if resp.getcode() != 200:
                raise error.HTTPError(
                    URL, resp.getcode(), resp.reason, resp.headers, None
                )
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except error.HTTPError:
        raise
    except error.URLError:
        raise


if __name__ == "__main__":
    data = download_data()
    with open("data/wl-current.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
