#!/usr/bin/python3
from flask import Flask,request,send_from_directory,render_template,abort
import pytesseract
from PIL import Image
from re import sub
from io import BytesIO
from flask_recaptcha import ReCaptcha
app = Flask(__name__)
app.config.update(
    RECAPTCHA_SITE_KEY = "6Lfn708UAAAAAIkaQ2up-kmJAskkulS6JCSHuXLD",
    RECAPTCHA_SECRET_KEY = open("private/config-9a9f05ed-e0d2-46f9-a761-89573214d6ff").readline(),
    MAX_CONTENT_LENGTH = 500 * 1024
)
recaptcha = ReCaptcha(app=app)
x = open("private/flag.txt").read()

@app.route('/',methods=['GET'])
def ind():
    return render_template("index.html")

@app.route('/debug',methods=['GET'])
def debug():
    return send_from_directory('./', "codeserver.py")

@app.route('/equation',methods=['POST'])
def equation():
    if recaptcha.verify():
        if 'file' not in request.files:
            return render_template('result.html', result = "No file uploaded")
        file = request.files['file']
        if file and file.filename == '':
            return render_template('result.html', result = "No correct file uploaded")
        if file:
            try:
                input_text = pytesseract.image_to_string(Image.open(BytesIO(file.read())))
                print(input_text)
                formated_text = "=".join(input_text.split("\n"))
                formated_text = formated_text.replace("=","==")
                formated_text = sub('===+','==',formated_text)
                formated_text = formated_text.replace(" ","")
                print(formated_text)
                if any(i not in 'abcdefghijklmnopqrstuvwxyz0123456789()[]=+-*' for i in formated_text):
                    return render_template('result.html', result = "Some features are still in beta !")
                if formated_text.count('(') > 1 or formated_text.count(')') > 1 or formated_text.count('[') > 1 or formated_text.count(']') > 1 :
                    return render_template('result.html', result = "We can not solve complex equations for now !")
                if any(i in formated_text for i in ["import","exec","compile","tesseract","chr","os","write","sleep"]):
                    return render_template('result.html', result = "We can not understand your equation !")
                if len(formated_text) > 15:
                    return render_template('result.html', result = "We can not solve complex equations for now !")
                if "==" in formated_text:
                    parts = formated_text.split("==",maxsplit=2)
                    pa_1 = int(eval(parts[0]))
                    pa_2 = int(eval(parts[1]))
                    if pa_1 == pa_2:
                        return render_template('result.html', result = "Wow, it works !")
                    else:
                        return render_template('result.html', result = "Sorry but it seems that %d is not equal to %d"%(pa_1,pa_2))
                else:
                    return render_template('result.html', result = "Please import a valid equation !")

            except (KeyboardInterrupt, SystemExit):
                raise
            except  Exception as e :
                print(e)
                return render_template('result.html', result = "Something went wrong...")
    else:
        return render_template('result.html', result = "Please be a human")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/private/flag.txt')
def censorship():
    abort(403)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
