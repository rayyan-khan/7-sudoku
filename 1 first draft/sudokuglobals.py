import sys, time

# input:
#INPUT = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('puzzle.txt', 'r')

# set up global variables:
#pzl = INPUT.readline()
INP = '1234567..'*9

def setGlobals(pzl):
    global PZLSIZE, CSTRSIZE, SUBHEIGHT, SUBWIDTH, SYMSET, ROWCSTR, COLCSTR, SUBCSTR, CSTRS

    pzl = ''.join([n for n in pzl if n != '.'])

    PZLSIZE = len(INP)
    CSTRSIZE = int(len(INP) ** .5)
    SUBHEIGHT, SUBWIDTH = int(CSTRSIZE ** .5), int(CSTRSIZE ** .5) \
        if int(CSTRSIZE ** .5 // 1) == int(CSTRSIZE ** .5) \
        else (int(CSTRSIZE ** .5 // 1), int(CSTRSIZE ** .5 // 1 + 1))

    if len({n for n in pzl}) - 1 == CSTRSIZE:
        SYMSET = {n for n in pzl} - {'.'}
    else:
        SYMSET = set([s for s in pzl]
                     + [k for k in '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'][:CSTRSIZE - len({n for n in pzl})])

    ROWCSTR = [{index for index in range(row*SUBWIDTH, row*SUBWIDTH + SUBWIDTH*SUBHEIGHT)}
           for row in range(CSTRSIZE)]
    COLCSTR = [{index for index in range(col, col + PZLSIZE - SUBWIDTH*SUBHEIGHT + 1, SUBWIDTH*SUBHEIGHT)}
               for col in range(CSTRSIZE)]
    SUBCSTR = [{boxRow + boxColOffset + subRow * CSTRSIZE + subCol
                for subRow in range(SUBHEIGHT) for subCol in range(SUBWIDTH)}
               for boxRow in range(0, PZLSIZE, SUBHEIGHT * CSTRSIZE) for boxColOffset in range(0, CSTRSIZE, SUBWIDTH)]
    CSTRS = ROWCSTR + COLCSTR + SUBCSTR

setGlobals(INP)

# helper methods
def printPzl(pzl):
    for row in range(int(len(pzl)**.5)):
        print(' '.join(pzl[row*SUBWIDTH: row*SUBWIDTH + SUBWIDTH*SUBHEIGHT]))

def checkSum(pzl):
    return sum(ord(n) for n in pzl) - PZLSIZE*ord('0')