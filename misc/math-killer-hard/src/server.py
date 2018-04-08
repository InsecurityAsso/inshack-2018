#!/usr/bin/python

#easy https://math-killer.ctf.insecurity-insa.fr/solve?a=-5&b=7&c=8
#hard https://math-killer.ctf.insecurity-insa.fr/solve?a=4373612677928697257861252602371390152816537558161613618621437993378423467772036&b=36875131794129999827197811565225474825492979968971970996283137471637224634055579&c=154476802108746166441951315019919837485664325669565431700026634898253202035277999

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/solve', methods=['GET'])
def get_coin():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        c = int(request.args.get('c'))
    except Exception:
        return jsonify({'status':'error','message':'Invalid parameters'})

    if ((a*(a+c)*(a+b))+(b*(b+a)*(b+c))+(c*(a+c)*(b+c)))%((a+c)*(b+c)*(a+b))==0 and ((a*(a+c)*(a+b))+(b*(b+a)*(b+c))+(c*(a+c)*(b+c)))/((a+c)*(b+c)*(a+b))==6:
        flags={'easy':'INSA{try_positive_solutions_now}'}
        if a>0 and b>0 and c>0:
            message = 'Congrats for solving hard mode ! you get both flags for free :)'
            flags['hard']='INSA{OMG_you_actually_killed_math}'
        else:
            message = 'Nice job , you solved easy mode ! Now get your math skills on'
   
        return jsonify({'status':'success','message':message,'flags':flags})
    return jsonify({'status':'fail','message':'Try again'})


if __name__ == '__main__':
    app.run("0.0.0.0")
