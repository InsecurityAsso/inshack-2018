from flask import Flask, request, make_response, render_template
import hashlib
import yaml
import random
import string
import time
import base64
import logging


def random_byte_str(n):
    return b''.join(random.SystemRandom().choice(string.ascii_letters + string.digits).encode() for _ in range(n))

PRIVATE_KEY = random_byte_str(20)
app = Flask(__name__)
VALID_CHARS_PERMISSIVE = string.printable.encode()
VALID_CHARS_STRICT = (string.ascii_letters + string.digits + '-.: _').encode()
FILES = {}
for f in ["basic", "premium"]:
    with open("files/" + f) as fh:
        FILES[f] = fh.read()

# Never trust user input
def strip_invalid(s, charset=VALID_CHARS_STRICT):
    res = ''
    for c in s:
        if c in charset:
            res += chr(c)
    return res


def sign(pk, salt, content):
    to_hash = pk + salt + content
    return hashlib.sha256(to_hash).hexdigest()


def generate_cookie(insa_coins=400, name="Adrian Lamo"):
    salt = random_byte_str(10)
    # Never trust user input
    name = strip_invalid(name.encode())
    yaml_document = yaml.dump({
        "name": name,
        "insa_coins": insa_coins,
        "valid_until": int(time.time()) + 10*60,  # Cookie only valid 10min
    }, default_flow_style=False)
    signature = sign(PRIVATE_KEY, salt, yaml_document.encode())
    encoded_serialized = base64.urlsafe_b64encode(yaml_document.encode()).decode()
    return '{}:{}:{}'.format(salt.decode(), signature, encoded_serialized)


def extract_user_info(cookie):
    salt, signature, encoded_serialized = cookie.split(":")
    yaml_document = base64.urlsafe_b64decode(encoded_serialized)
    assert sign(PRIVATE_KEY, salt.encode(), yaml_document) == signature, "Stop it, you clever(ish) hax0r!"
    # Never trust user input
    yaml_document = strip_invalid(yaml_document, VALID_CHARS_PERMISSIVE)
    user = yaml.safe_load(yaml_document)
    assert user is not None, "This document is empty?? Something went wrong!"
    assert len({"name", "insa_coins", "valid_until"} - set(user.keys())) == 0, "Expected keys were not present"
    assert time.time() < user["valid_until"], "Too late! Your files are lost :'("
    return user


@app.route('/', methods=["GET"])
def home():
    user_cookie = request.cookies.get("user")
    if not user_cookie:
        user_cookie = generate_cookie()
    try:
        user = extract_user_info(user_cookie)
    except Exception as e:
        resp = make_response(render_template("error.html", error=str(e)))
        resp.set_cookie("user", generate_cookie())
        return resp
    # Never trust user input
    name = strip_invalid(user["name"].encode())
    resp = make_response(render_template("index.html", insa_coins=user["insa_coins"], name=name))
    resp.set_cookie("user", user_cookie)
    return resp


@app.route('/pay', methods=["POST"])
def pay():
    if set(request.args.keys()) != {"cost", "offer"}:
        return render_template("error.html", error="Wrong params")
    fnames = {
        "basic": "Not_so_important_file",
        "premium": "Your_precious_files",
    }
    try:
        cost = int(request.args["cost"])
        f = request.args["offer"]
        assert f in fnames
        assert cost > 0
    except Exception:
        return render_template("error.html", error="Wrong params")
    if f == "premium" and cost != 500:
        return render_template("error.html", error="Those files look precious to you, It will cost a lot to decrypt them.")

    user_cookie = request.cookies.get("user")
    if not user_cookie:
        return render_template("error.html", error="you has no coin, pleaze go by some!")
    try:
        user = extract_user_info(user_cookie)
    except Exception as e:
        return make_response(str(e))

    insa_coins = user["insa_coins"]
    if insa_coins < cost:
        return render_template("error.html", error="You don't have enough INShAcoins to decrypt this file, please go buy some")
    insa_coins -= cost

    resp = make_response(render_template("success.html", message=FILES.get(f, b'')))
    user_cookie = generate_cookie(insa_coins=insa_coins, name=user["name"])
    resp.set_cookie("user", user_cookie)

    return resp


@app.route('/change-name', methods=["POST"])
def change_name():
    if set(request.form.keys()) != {"name"}:
        return render_template("error.html", error="Wrong params")
    new_name = request.form["name"]
    if not isinstance(new_name, str):
        return render_template("error.html", error="Wrong params")
    # Never trust user input
    new_name = strip_invalid(new_name.encode())
    user_cookie = generate_cookie(name=new_name)
    try:
         user = extract_user_info(user_cookie)
    except Exception as e:
         return str(e)

    resp = make_response("Thanks <i>{}</i>, now you can <a href='/'>pay us</a>.".format(user["name"]))
    resp.set_cookie("user", user_cookie)
    return resp


if __name__ == "__main__":
    app.run("0.0.0.0")

