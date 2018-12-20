import sys, time

# need to fix bug

# input:
INPUT = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('puzzles.txt', 'r')

# set up global variables:
INP = '.'*81

def setGlobals(pzl):
    global PZLSIZE, CSTRSIZE, SUBHEIGHT, SUBWIDTH, SYMSET, ROWCSTR, COLCSTR, SUBCSTR, CSTRS, NBRS

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

    ROWCSTR = [{index for index in range(row*CSTRSIZE, (row + 1)*CSTRSIZE)}
           for row in range(CSTRSIZE)]
    COLCSTR = [{index for index in range(col, col + PZLSIZE - SUBWIDTH*SUBHEIGHT + 1, SUBWIDTH*SUBHEIGHT)}
               for col in range(CSTRSIZE)]
    SUBCSTR = [{boxRow + boxColOffset + subRow * CSTRSIZE + subCol
                for subRow in range(SUBHEIGHT) for subCol in range(SUBWIDTH)}
               for boxRow in range(0, PZLSIZE, SUBHEIGHT * CSTRSIZE) for boxColOffset in range(0, CSTRSIZE, SUBWIDTH)]
    CSTRS = ROWCSTR + COLCSTR + SUBCSTR
    NBRS = [set().union(*[cset for cset in CSTRS if n in cset]) - {n} for n in range(PZLSIZE)]

setGlobals(INP)

# helper methods
def printPzl(pzl):
    cstrsize = int(len(pzl) ** .5)
    subheight, subwidth = int(cstrsize ** .5), int(cstrsize ** .5) \
        if int(cstrsize ** .5 // 1) == int(cstrsize ** .5) \
        else (int(cstrsize ** .5 // 1), int(cstrsize ** .5 // 1 + 1))
    rowLen = subwidth*(int(cstrsize/subheight))
    for row in range(cstrsize):
        print(' '.join(pzl[rowLen*row: rowLen*(row + 1)]))


def checkSum(pzl):
    return sum(ord(n) for n in pzl) - PZLSIZE*ord('0')

# solve
def solve(pzl):
    openPos = pzl.find('.')
    if openPos == -1:
        return pzl
    for sym in SYMSET - {pzl[n] for n in NBRS[openPos]}:
        pzlMove = pzl[:openPos] + sym + pzl[openPos + 1:]
        newPzl = solve(pzlMove)
        if newPzl:
            return newPzl
    return ''


# run
time51 = time.clock()
for line in enumerate(INPUT.readlines()):
    start = time.clock()
    pzlNum, INP = line
    if pzlNum == 50:
        print('Time for 51: {}'.format(time.clock() - time51))
    INP = INP.strip()
    setGlobals(INP)
    solution = solve(INP)
    print('{}: Time: {} Sum: {} \n'.format(pzlNum + 1, round(time.clock() - start, 3), checkSum(solution)), end='')
    if solution == '':
        print('No solution -- i.e. theres a bug here')
