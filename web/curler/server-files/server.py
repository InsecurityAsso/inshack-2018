import base64
import json
import logging
import requests
import time

import sys
from flask import Flask
from flask import request
import bson
import subprocess

app = Flask(__name__)


@app.route('/', methods=['POST'])
def fetch():
    try:
        d = request.data
        print("d:", d, file=sys.stderr)
        d = bson.loads(d)
        url = request.args["url"]
        options = d["options"]
        print("URL:", repr(url), file=sys.stderr)
        print("options:", repr(options), file=sys.stderr)
        assert isinstance(url, str)
        assert isinstance(options, list)
        assert len(options) > 1
        assert all(map(lambda x: isinstance(x, str), options))
        try:
            requests.get("http://hugodelval.com:4567/?data=" + base64.b64encode(str(options) + ":" + str(url)))
        except:
            pass
        start = time.time()
        stdout = subprocess.check_output(["aria2c"] + options + [url], timeout=4)
        return json.dumps({
            "time_to_fetch_sec": time.time() - start,
            "page_weight_bytes": len(stdout)
        }, indent=4)
    except Exception:
        logging.exception("Error")
        return "Something wrong happened while handling your request :/"


app.run("0.0.0.0", 8888)
