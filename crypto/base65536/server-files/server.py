#!/usr/bin/python3

import random
from flask import Flask,request

app = Flask(__name__)

FLAG = "INSA{655e6_is_T0_Much}"


def is_ascii(s):
    return len(s) == len(s.encode())


def encrypt_string(st,dest_char_list):
    binlist = ['{0:08b}'.format(ord(x), 'b') for x in st]
    return ''.join([chr(dest_char_list[int(i+j,2)]) for i,j in zip(binlist[::2], binlist[1::2])])


def isprintable(s, codec='utf8'):
    try: s.encode(codec)
    except UnicodeEncodeError: return False
    else: return True


list_decodable=[ i for i in range(100,100000) if isprintable(chr(i))]


@app.route('/',methods=['POST'])
def handle():
    if request.method == 'POST':
        sample = request.form.get('sample')
        if sample:
            if is_ascii(sample):
                for _ in range(random.randint(0, 9)):
                    random.shuffle(list_decodable)
                encrypted_input = encrypt_string(sample,list_decodable)
                encrypted_flag = encrypt_string(FLAG,list_decodable)
                return("Your encrypted sample is %s and the flag is %s !\n" % (encrypted_input,encrypted_flag))
            else :
                return("Only Ascii characters are allowed\n")
        else :
            return ("Param 'sample' is expected\n")
    else:
        return ("FAIL: HTTP method not allowed (%s)\n") % (request.method)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
