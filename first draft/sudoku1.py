import sys, time

# input:
#INPUT = open(sys.argv[1], 'r') if len(sys.argv) == 2 else open('puzzle.txt', 'r')

# set up global variables:
#pzl = INPUT.readline()
INP = '1234567..'*9
pzl = ''.join([n for n in INP if n != '.'])

PZLSIZE = len(INP)
CSTRSIZE = int(len(INP)**.5)
SUBHEIGHT, SUBWIDTH = int(CSTRSIZE**.5), int(CSTRSIZE**.5) \
    if int(CSTRSIZE**.5//1) == int(CSTRSIZE**.5) \
    else (int(CSTRSIZE**.5//1), int(CSTRSIZE**.5//1+1))

if len({n for n in pzl}) == CSTRSIZE:
    SYMSET = {n for n in pzl}
else:
    SYMSET = set([s for s in pzl]
                 + [k for k in '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'][:CSTRSIZE-len({n for n in pzl})])

ROWCSTR = {row: {index for index in range(row*SUBWIDTH, row*SUBWIDTH + SUBWIDTH*SUBHEIGHT)}
           for row in range(CSTRSIZE)}
COLCSTR = {col: {index for index in range(col, col + PZLSIZE - SUBWIDTH*SUBHEIGHT + 1,
                                          SUBWIDTH*SUBHEIGHT)} for col in range(CSTRSIZE)}
SUBCSTR = {}

for subcstr in range(CSTRSIZE): # this is wrong
    print(subcstr)
    print(SUBCSTR)
    SUBCSTR[subcstr] = set()
    for index in range(PZLSIZE):
        row = index % CSTRSIZE
        col = index // CSTRSIZE
        if row in range(row * subcstr, row * subcstr + SUBWIDTH) \
                and col in range(col*subcstr, col*subcstr + SUBHEIGHT):
            if SUBCSTR[subcstr]:
                SUBCSTR[subcstr].add(index)
            else:
                SUBCSTR[subcstr] = {index}

print(SUBCSTR)

# helper methods
def printPzl(pzl):
    for row in range(int(len(pzl)**.5)):
        print(' '.join(pzl[row*SUBWIDTH: row*SUBWIDTH + SUBWIDTH*SUBHEIGHT]))

def checkSum(pzl):
    return sum(ord(n) for n in pzl) - PZLSIZE*ord('0')


'''
constraintSets
3n constraints
list of constraints
dicts - row/col/subblock constraint identifiers
neighbors is list where index is string index in pzl and value is the set of neighbor positions
output = 
puzzle num, puzzle
puzzle solution, checkSum
nqueens*numsymbols basically
remember to add stuff at the beginning
due friday
'''