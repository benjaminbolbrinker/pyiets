def readGreen(greenmatrixfile):
    with open(greenmatrixfile, 'r') as greenfile:
        rawinput = greenfile.readlines()
    print(rawinput)
