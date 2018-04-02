#!/usr/bin/env python3
"""
This script is a CLI to ban IP in a distributed fashion (ie in all our servers
at the same time).
"""
import os
import subprocess
import sys
from lib import Script

KNOWN_HOSTS = "./known_hosts"
PRIVATE_KEY = "/Users/lmartine/.ssh/id_ecdsa"

class BanIP(Script):
    def __init__(self, *args, **kwargs):
        pass

    def run(self):
        env = os.environ.copy()
        env["ANSIBLE_HOST_KEY_CHECKING"] = "false"
        process = subprocess.Popen(["ansible", "all", "-a", "date", "-f", "10", "--inventory-file", "/Users/lmartine/.homebrew/bin/terraform-inventory", "-u", "root"], shell=True, cwd="/Users/lmartine/Documents/perso/inshack-2018/infra/terraform", stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

        while True:
            status = process.poll()
            if status is not None:
                break
        for line in process.stderr:
            sys.stdout.write(str(line))
            print(line)

if __name__ == "__main__":
    cli = BanIP()
    cli.run()
