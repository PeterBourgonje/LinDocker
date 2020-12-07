#!/usr/bin/python3

import os
import sys
import time
import json
import codecs
import argparse
import subprocess

from flask import Flask, Response
from flask import request
from flask_cors import CORS

import convert

app = Flask(__name__)
CORS(app)

INOUTFOLDER = 'inputoutput'

@app.route('/parse', methods=['GET', 'POST'])
def parse():

    inp = None
    if request.args.get('input'):
        inp = request.args.get('input')
    elif request.files['input']:
        inp = request.files['input'].read().decode('utf-8')
    else:
        return 'INFO: Please provide input text.\n'

    docid = None
    if request.args.get('docid') == None:
        docid = time.strftime('%Y%m%d%H%M%S', time.gmtime())
    else:
        docid = request.args.get('docid')

    f = os.path.join(INOUTFOLDER, docid+'.txt')
    codecs.open(f, 'w').write(inp)
    
    subprocess.call(['java', '-jar', 'parser.jar', f])

    pipefile = os.path.join(INOUTFOLDER, 'output', docid+'.txt.pipe')
    if not os.path.exists(pipefile):
        return 'ERROR: No output file generated. Something went wrong...\n'
    pdtb_pipe_output = codecs.open(pipefile, 'r').readlines()

    relations = convert.pipe2json(docid, pdtb_pipe_output, os.path.join(INOUTFOLDER, 'output', docid+'.txt.ptree.csv')) # passing on ptree as last arg here to take tokenisation from there (doing it myself again takes extra time and, more importantly, may result in tokenisation differences)
    

    return json.dumps(relations)#, indent=2, sort_keys=True)
    
if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--port", help="port number to start flask app on", default=5000, type=int)
    args = argparser.parse_args()

    if not os.path.exists(INOUTFOLDER):
        os.makedirs(INOUTFOLDER)
    
    app.run(host='0.0.0.0', port=args.port)
