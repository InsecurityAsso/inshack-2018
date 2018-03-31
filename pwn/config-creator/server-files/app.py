import string

VALID_CHARS = {c for c in string.digits + string.ascii_letters + "(),[]"}

LOCALS = {}


def strip_invalid(string):
    res = ''
    for c in string:
        if c in VALID_CHARS:
            res += c
    return res


def _build_template():
    tpl = 'f"""\nconfiguration [\n'
    for key in LOCALS:
        tpl += f"    {key} = {{{key}}};\n"
    return tpl + ']\n"""'


def register_new_entry():
    key = input("Config key? ")
    key = strip_invalid(key)
    value = input("Config value? ")
    LOCALS[key] = value


def change_existing_value():
    key = input("Config key? ")
    key = strip_invalid(key)
    if not key in LOCALS:
        print("Sorry, key not found in current configuration")
        return
    value = input("Config value? ")
    LOCALS[key] = value


def show_template():
    print("template:")
    print(_build_template())


def show_config():
    print("config:")
    print(eval(_build_template(), {}, LOCALS))


print("Welcome to the config creator!")

while True:
    print()
    print("Please choose your action:")
    print("  1. Register a new config entry")
    print("  2. Change value of an existing config entry")
    print("  3. Show my template")
    print("  4. Show my config")
    print("  5. Reset current config")
    print("  6. exit")
    print()
    try:
        choice = input("Choice? ")
        assert choice in {"1", "2", "3", "4", "5", "6"}
    except Exception:
        print("Wrong choice, try again")
        continue
    except KeyboardInterrupt:
        print("Bye")
        exit(0)

    print()
    try:
        if choice == "1":
            register_new_entry()
        elif choice == "2":
            change_existing_value()
        elif choice == "3":
            show_template()
        elif choice == "4":
            show_config()
        elif choice == "5":
            LOCALS = {}
            print("Done.")
        elif choice == "6":
            print("Bye")
            exit(0)
    except Exception as e:
        print(e)
        print("An error occured, sorry")
        continue
    except KeyboardInterrupt:
        print("Bye")
        exit(0)
