import json


def infile(inputfilename):
    with open(inputfilename, 'r') as infile:
        indata = json.load(infile)
    return indata
