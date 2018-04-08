import shlex
import subprocess
import random
import string
import os
import sys

if os.path.exists("/.dockerenv"):
    subprocess.run(["rm", "app.py"])


def rand_string(n):
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(n)])


allowed_commands = {"ls", "cat", "openstack"}
allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
openstack_authorized_commands = {'user', 'keypair', 'extension', 'ip', 'volume', 'compute', 'network', 'subnet', 'snapshot', 'object', 'command', 'ec2', 'security', 'console', 'port', 'role', 'flavor', 'configuration', 'limits', 'aggregate', 'container', 'service', 'quota', 'catalog', 'floating', 'consistency', 'host', 'endpoint', 'hypervisor', 'project', 'help', 'module', 'availability', 'router', 'server', 'token', 'usage', 'complete', 'address', 'image'}

print("""
 ██████╗ ██████╗ ███████╗███╗   ██╗███████╗████████╗ █████╗  ██████╗██╗  ██╗      █████╗  █████╗ ███████╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝     ██╔══██╗██╔══██╗██╔════╝
██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗   ██║   ███████║██║     █████╔╝█████╗███████║███████║███████╗
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██╔═██╗╚════╝██╔══██║██╔══██║╚════██║
╚██████╔╝██║     ███████╗██║ ╚████║███████║   ██║   ██║  ██║╚██████╗██║  ██╗     ██║  ██║██║  ██║███████║
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

""")
print("Available commands are: ls, cat, openstack")
print("Note: we're only showing you stdout\n")


def quit_shell():
    print("\nBye.")
    exit(0)


while True:
    try:
        cmd = input("$ ")
        if cmd.lower() == "exit" or cmd == "0x4":
            quit_shell()
        assert len(cmd) < 500, "Command too long"
        assert "flag.txt" not in cmd, "Command failed, I don't like this word"
        assert all(map(lambda c: c in allowed_chars, cmd)), "I don't like this char"
        user_command = shlex.split(cmd)
    except AssertionError as e:
        print(str(e))
        continue
    except (EOFError, KeyboardInterrupt):
        quit_shell()
    except Exception:
        print("Wrong command, skipping")
        continue

    skip = False

    if not user_command:
        continue
    if not user_command[0] in allowed_commands:
        print("Command not allowed")
        continue
    if user_command[0] == "cat":
        print("Maybe it's not the real cat.. Maybe you should look somewhere else, idk ¯\_(ツ)_/¯")
        continue
    if user_command[0] == "ls":
        for opt in user_command[1:]:
            if not opt.startswith("-") and opt not in {".", "./"}:
                print("Sorry, you can only see the current directory (`ls -la` for example)")
                skip = True
    if user_command[0] == "openstack":
        non_options_params = list(filter(lambda c: not c.startswith('-'), user_command))
        if len(user_command) == 2 and user_command[1] in {"--help", "-h", "--version"}:
            # ok
            pass
        elif len(user_command) == 3 and user_command[2] in {"--help", "-h", "--version"} and user_command[1] == "--debug":
            # ok
            pass
        elif len(non_options_params) <= 1:
            print("Interactive mode disabled for simplicity.")
            continue
        else:
            if non_options_params[1] not in openstack_authorized_commands:
                print("Sorry this openstack command is unknown. See openstack --help")
                skip = True

    if skip:
        continue

    print(user_command, file=sys.stderr, flush=True)
    print("Processing...", flush=True)
    try:
        subprocess.run(user_command, timeout=60)
    except Exception:
        break
