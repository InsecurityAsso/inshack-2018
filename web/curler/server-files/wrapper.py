import logging

import bson
import json
import sys
from urllib.parse import urlparse
from http.client import HTTPConnection

fetcher_service = sys.argv[1]
fetch_options = {
    "timeout": {
        "key": "--timeout",
        "value": 2,
        "allowed_values": {1, 2, 3},
    },
    "connect timeout": {
        "key": "--connect-timeout",
        "value": 2,
        "allowed_values": {1, 2, 3},
    },
    "dry run": {
        "key": "--dry-run",
        "value": False,
        "allowed_values": {True, False},
    },
    "max tries": {
        "key": "--max-tries",
        "value": 5,
        "allowed_values": {i for i in range(10)},
    },
}
url_to_fetch = "http://insecurity-insa.fr"

print("Welcome to your FaaS (Fetcher as a Service)!")
print("This program allows you to fetch some stats on a given web url.")


def _load_from_stdin(msg):
    return json.loads(input(msg))


def change_config():
    global fetch_options
    print("Configurable options:\n  - {}".format("\n  - ".join(fetch_options.keys())))
    config = input("Which config do you want to change? ")
    assert config in fetch_options, "Configuration option not found"
    new_config_value = _load_from_stdin("New value for '{}'? ".format(config))
    assert isinstance(new_config_value, type(fetch_options[config]["value"])), "Wrong type for new config value"
    assert new_config_value in fetch_options[config]["allowed_values"], "New config value not in allowed set"
    fetch_options[config]["value"] = new_config_value


def choose_url():
    url = _load_from_stdin("Url? ")
    logging.error(url)
    parsed = urlparse(url)
    assert isinstance(url, str), "Url should be a string"
    assert url.startswith("http://"), "Sorry, only http is available for now"
    assert parsed.scheme and parsed.netloc and parsed.path
    global url_to_fetch
    url_to_fetch = url
    print("Url successfully changed")


def fetch():
    # Hit local flask server
    conn = HTTPConnection(fetcher_service, 8888)
    options = []
    for conf in fetch_options.values():
        options.append(conf["key"] + "=" + str(conf["value"]).lower())
    params = bson.dumps({
        "options": options
    })
    conn.request("POST", "/?url=" + url_to_fetch, params)
    response = conn.getresponse()
    print("Stats:")
    print(response.read().decode())
    print()


while True:
    print()
    print("Current config is:")
    print("URL to fetch: {}".format(url_to_fetch))
    print("Fetcher options: {}".format({k: v["value"] for k, v in fetch_options.items()}))
    print()
    print("Please choose your action:")
    print("  1. Change the default configuration of our fetcher")
    print("  2. Choose the URL you want us to inspect")
    print("  3. Fetch!")
    print("  4. Exit")
    print()
    try:
        choice = input("Choice? ")
        assert choice in {"1", "2", "3", "4"}
    except Exception:
        print("Wrong choice, try again")
        continue
    except KeyboardInterrupt:
        print("Bye")
        exit(0)

    print()
    try:
        if choice == "1":
            change_config()
        elif choice == "2":
            choose_url()
        elif choice == "3":
            fetch()
        elif choice == "4":
            print("Bye")
            exit(0)
    except Exception:
        logging.exception("Error while handling user's request")
        print("An error occurred, sorry")
        continue
    except KeyboardInterrupt:
        print("Bye")
        exit(0)
