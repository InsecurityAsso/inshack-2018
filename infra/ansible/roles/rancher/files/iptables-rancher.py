#/usr/bin/python3
import subprocess
import time

class IptablesLog:
    def __init__(self, *args, **kwargs):
        self.running = True

    def start(self):
        while self.running:
            try:
                result = []
                result = subprocess.check_output("iptables -t nat -nvL PREROUTING --line-numbers | tail -n +3", shell=True).decode()
                result = result.split('\n')
                found = False
                for line in result:
                    line = line.split()
                    if not line:
                        continue

                    line_number = int(line[0])
                    line = " ".join(line)

                    if "RATE_LIMIT" in line:
                        found = True
                        if not line.startswith("1 "):
                            subprocess.check_output("iptables -t nat -D PREROUTING {}".format(line_number), shell=True)
                            self.add_rules()
                        break

                if not found:
                    self.add_rules()

                time.sleep(1)

            except Exception as e:
                # Loggs any error that happened along with the stack trace
                print(e)

    def add_rules(self):
        subprocess.check_output("iptables -t nat -I PREROUTING 1 -i ens3 -p tcp -m multiport --dports 80,443,10000:20000 -j RATE_LIMIT", shell=True)

if __name__ == "__main__":
    daemon = IptablesLog()
    daemon.start()
