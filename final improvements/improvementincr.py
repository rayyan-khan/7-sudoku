import sys, time

# input:
INPUT = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('puzzles.txt', 'r')

# set up global variables:
INP = '.'*81

# just for self-reference:
'''
NBRS = {index: {neighboring indexes}}
INDSYM = {index: {possible symbols}}

'''

def setGlobals(pzl):
    global PZLSIZE, CSTRSIZE, SUBHEIGHT, SUBWIDTH, SYMSET, ROWCSTR, COLCSTR, SUBCSTR, CSTRS, NBRS, INDSYM

    pzl = ''.join([n for n in pzl if n != '.'])

    PZLSIZE = len(INP)
    CSTRSIZE = int(len(INP) ** .5)
    SUBHEIGHT, SUBWIDTH = int(CSTRSIZE ** .5), int(CSTRSIZE ** .5) \
        if int(CSTRSIZE ** .5 // 1) == int(CSTRSIZE ** .5) \
        else (int(CSTRSIZE ** .5 // 1), int(CSTRSIZE ** .5 // 1 + 1))

    SYMSET = {n for n in pzl} - {'.'}
    if len(SYMSET) != CSTRSIZE:
        otherSyms = [n for n in '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0']
        while len(SYMSET) < CSTRSIZE:
            SYMSET.add(otherSyms.pop(0))

    ROWCSTR = [{index for index in range(row*CSTRSIZE, (row + 1)*CSTRSIZE)}
           for row in range(CSTRSIZE)]
    COLCSTR = [{index for index in range(col, col + PZLSIZE - SUBWIDTH*SUBHEIGHT + 1, SUBWIDTH*SUBHEIGHT)}
               for col in range(CSTRSIZE)]
    SUBCSTR = [{boxRow + boxColOffset + subRow * CSTRSIZE + subCol
                for subRow in range(SUBHEIGHT) for subCol in range(SUBWIDTH)}
               for boxRow in range(0, PZLSIZE, SUBHEIGHT * CSTRSIZE) for boxColOffset in range(0, CSTRSIZE, SUBWIDTH)]
    CSTRS = ROWCSTR + COLCSTR + SUBCSTR
    NBRS = [set().union(*[cset for cset in CSTRS if n in cset]) - {n} for n in range(PZLSIZE)]

    INDSYM = {index: SYMSET - {INP[n] for n in NBRS[index]} for index in range(PZLSIZE) if INP[index] == '.'}
    print('INDSYM:', INDSYM)


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


def getBestPos(pzl):
    mostConstrained = 0 # number of syms already placed in NBRS[index] -- larger = fewer options
    bestPos = set()
    for pos in INDSYM: # for each unfilled position in pzl
        numSyms = len(INDSYM[pos]) # find the number of syms placed
        if numSyms > mostConstrained: # if its bigger than the current biggest
            mostConstrained = numSyms # set it as the biggest
            bestPos = set() # and reset bestPos
        if numSyms == mostConstrained: # otherwise if equal to current greatest number of syms placed
            bestPos.add(pos) # add it to the set of best positions
    return bestPos

def getBestSyms(pzl):
    bestSyms = set()
    mostPlaced = 0
    for sym in SYMSET:
        placed = pzl.count(sym)
        if placed > mostPlaced:
            mostPlaced = placed
            bestSyms = set()
        if placed == mostPlaced:
            bestSyms.add(sym)
    return bestSyms

def updateIndSym(updatedInd, sym, indSyms):
    for nbr in NBRS[updatedInd]:
        if indSyms.get(nbr, None) == sym:
            return False
        elif nbr in indSyms:
            indSyms[nbr] = indSyms[nbr] - {sym}
        else: return False
    indSyms.pop(updatedInd)  # remove as possible
    return indSyms

def restoreIndSym(updatedInd, sym, updatedSyms):
    for nbr in NBRS[updatedInd]:
        if nbr in updatedSyms:
            updatedSyms[nbr].add(sym)
    return updatedSyms

# solve
def solve(pzl, indSyms):
    if pzl.find('.') == -1:
        return pzl

    bestPos = getBestPos(pzl)

    for pos in bestPos:
        for sym in indSyms[pos]:

            newIndSyms = updateIndSym(pos, sym, indSyms)
            if indSyms:
                pzlMove = pzl[:pos] + sym + pzl[pos + 1:]
                newPzl = solve(pzlMove, newIndSyms)
                if newPzl:
                    return newPzl
                indSyms = restoreIndSym(pos, sym, newIndSyms)
    return ''


# run
time51 = time.clock()
totalTime = time.clock()
for line in enumerate(INPUT.readlines()):
    start = time.clock()
    pzlNum, INP = line
    print('Puzzle:', pzlNum + 1, '\nOriginal:', line[1], end='')
    if pzlNum == 50:
        print('Time for 51: {}'.format(time.clock() - time51))
    INP = INP.strip()
    setGlobals(INP)
    solution = solve(INP, INDSYM)
    print('Solution: {} \nTime: {} Sum: {} \n'.format(solution, round(time.clock() - start, 3), checkSum(solution)))
    if solution == '':
        print('No solution -- i.e. theres a bug here')
print('Total Time:', round(time.clock()-totalTime, 3))
