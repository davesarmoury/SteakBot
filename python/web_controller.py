#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask_cors import CORS
from distutils import util

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/settings")
def updateSettings():
    data = {}
    data["meat"] = int(request.args.get("meat"))
    data["cook"] = int(request.args.get("cook"))

    outFile = open("steak.yaml", 'w')
    outFile.write(dump(data, Dumper=Dumper))
    outFile.close()

    line = "Received <" + str(data["meat"]) + ", " + str(data["cool"]) + ">"
    print(line)
    return line

def main():
    app.run("0.0.0.0")

main()
