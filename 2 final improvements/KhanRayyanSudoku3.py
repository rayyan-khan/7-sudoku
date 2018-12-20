import sys, time

# input:
INPUT = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('puzzles.txt', 'r')

# set up global variables:
INP = '.' * 81

# just for self-reference:
'''
NBRS = {index: {neighboring indexes}}
INDSYM = {index: {possible symbols}}

'''


def setGlobals(pzl):
    global PZLSIZE, CSTRSIZE, SUBHEIGHT, SUBWIDTH, SYMSET, ROWCSTR, COLCSTR, SUBCSTR, CSTRS, NBRS, STATS

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

    ROWCSTR = [{index for index in range(row * CSTRSIZE, (row + 1) * CSTRSIZE)}
               for row in range(CSTRSIZE)]
    COLCSTR = [{index for index in range(col, col + PZLSIZE - SUBWIDTH * SUBHEIGHT + 1, SUBWIDTH * SUBHEIGHT)}
               for col in range(CSTRSIZE)]
    SUBCSTR = [{boxRow + boxColOffset + subRow * CSTRSIZE + subCol
                for subRow in range(SUBHEIGHT) for subCol in range(SUBWIDTH)}
               for boxRow in range(0, PZLSIZE, SUBHEIGHT * CSTRSIZE) for boxColOffset in range(0, CSTRSIZE, SUBWIDTH)]
    CSTRS = ROWCSTR + COLCSTR + SUBCSTR
    NBRS = [set().union(*[cset for cset in CSTRS if n in cset]) - {n} for n in range(PZLSIZE)]

    STATS = {'returning new pzl': 0, 'recursing now': 0, 'updating indSym': 0, 'restoring indsym': 0}

    indsym0 = {index: SYMSET - {INP[n] for n in NBRS[index]} for index in range(PZLSIZE) if INP[index] == '.'}
    return indsym0


# helper methods
def printPzl(pzl):
    cstrsize = int(len(pzl) ** .5)
    subheight, subwidth = int(cstrsize ** .5), int(cstrsize ** .5) \
        if int(cstrsize ** .5 // 1) == int(cstrsize ** .5) \
        else (int(cstrsize ** .5 // 1), int(cstrsize ** .5 // 1 + 1))
    rowLen = subwidth * (int(cstrsize / subheight))
    for row in range(cstrsize):
        print(' '.join(pzl[rowLen * row: rowLen * (row + 1)]))


def checkSum(pzl):
    return sum(ord(n) for n in pzl) - PZLSIZE * ord('0')


def getBestPos(indSyms):
    # print(indSyms.keys())
    mostConstrained = CSTRSIZE  # number of syms already placed in NBRS[index] -- larger = fewer options
    bestPos = set()
    for pos in indSyms:  # for each unfilled position in pzl
        numSyms = len(indSyms[pos])  # find the number of syms placed
        if numSyms < mostConstrained:  # if its bigger than the current biggest
            mostConstrained = numSyms  # set it as the biggest
            bestPos = set()  # and reset bestPos
            bestPos.add(pos)
        #if numSyms == mostConstrained:  # otherwise if equal to current greatest number of syms placed
        #    bestPos.add(pos)  # add it to the set of best positions
    #print([len(indSyms[key]) for key in indSyms])
    #print(bestPos)
    return bestPos

def updateIndSym(updatedInd, sym, indSyms, pzl):
    STATS['updating indSym'] += 1
    for nbr in NBRS[updatedInd]:
        #if nbr not in indSyms and pzl[nbr] == sym:
            # print('nbr {} not in indsyms {}'.format(nbr, indSyms))
        #    return False
        if nbr in indSyms:
            indSyms[nbr] = indSyms[nbr] - {sym}
    #print('updatedInd: {}, pzl: {}, indSyms: {}'.format(updatedInd, pzl, indSyms))
    #try:
    print('updated index', indSyms.pop(updatedInd), updatedInd)  # remove as possible
    #except:
    #    pass #print('Indsyms {}, updatedInd {}'.format(indSyms, updatedInd))
    return indSyms


def restoreIndSym(updatedInd, sym, updatedSyms):  # not using
    STATS['restoring indsym'] += 1
    for nbr in NBRS[updatedInd]:
        if nbr in updatedSyms:
            updatedSyms[nbr].add(sym)
    return updatedSyms


# solve
def solve(pzl, indSyms):
    STATS['recursing now'] += 1
    if pzl.find('.') == -1 or not indSyms:
        return pzl

    bestPos = getBestPos(indSyms)
    # print('bestPos', bestPos)

    for pos in bestPos:
        #if len(indSyms[pos]) > 3:
        #    print('Pos: {} Choices {} lenBestPos {} bestPosSet {}'.format(pos, indSyms[pos], len(bestPos), bestPos))
        #    printPzl(pzl)
        #    exit()
        for sym in indSyms[pos]:
            newIndSyms = {pos: {s for s in indSyms[pos]} for pos in indSyms}
            for nbr in NBRS[pos]:
                if nbr not in indSyms and pzl[nbr] == sym:
                    continue
                if nbr in indSyms:
                    newIndSyms[nbr].discard(sym)
            del newIndSyms[pos]
            # print('indSymsCopy', indSymsCopy)
            #newIndSyms = updateIndSym(pos, sym, indSymsCopy, pzl)

            # print('newIndSyms', newIndSyms)
            #if newIndSyms != False:
            pzlMove = pzl[:pos] + sym + pzl[pos + 1:]
            newPzl = solve(pzlMove, newIndSyms)
            if newPzl:
                STATS['returning new pzl'] += 1
                return newPzl
            #indSyms = restoreIndSym(pos, sym, newIndSyms)
    return ''


# run
time51 = time.clock()
totalTime = time.clock()
for line in enumerate(INPUT.readlines()):
    start = time.clock()
    pzlNum, INP = line
    #if pzlNum > 51: continue
    print('Puzzle:', pzlNum + 1, '\nOriginal:', line[1], end='')
    if pzlNum == 50:
        print('Time for 51: {}'.format(time.clock() - time51))
    INP = INP.strip()
    indsym1 = setGlobals(INP)
    solution = solve(INP, indsym1)
    print('Solution: {} \nTime: {} Sum: {} \n'.format(solution, round(time.clock() - start, 3), checkSum(solution)),
          end='')
    if solution == '':
        print('No solution -- i.e. theres a bug here on puzzle', pzlNum)
        print(STATS)
print('Total Time:', round(time.clock() - totalTime, 3))
