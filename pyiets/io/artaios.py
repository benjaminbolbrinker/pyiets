import re
#  import numpy as np


def readComplex(rawstr):
    pass


def readGreen(greenmatrixfile):
    with open(greenmatrixfile, 'r') as greenfile:
        rawinput = greenfile.readlines()[1:]

    line = rawinput[0]
    #  floating_point = r'[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?'
    floating_point = r'[-+]?\d+[.][Ee0-9+-]+'
    #  print(line)
    for line in rawinput:
        ss = re.findall('[(] *' + floating_point + ', *' +
                        floating_point + ' *[)]', line)

        pass
    #  print(rawinput)
