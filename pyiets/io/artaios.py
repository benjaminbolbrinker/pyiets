import re
import numpy as np


def readGreen(greenmatrixfile):
    with open(greenmatrixfile, 'r') as greenfile:
        rawinput = greenfile.readlines()[1:]

    line = rawinput[0]
    floating_point = r'[-+]?\d+[.][Ee0-9+-]+'
    greenmatrix = []
    for line in rawinput:
        arr = re.findall('[(] *' + floating_point + ', *' +
                         floating_point + ' *[)]', line)
        arr = [np.fromstring(rawcomplex.replace('(', '').replace(')', ''),
                             sep=', ')
               for rawcomplex in arr]
        arr = [complex(*complexlist) for complexlist in arr]
        greenmatrix.append(arr)
    return np.array(greenmatrix)
