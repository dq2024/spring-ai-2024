class Peg:
    def __init__(self, hole, time):
        self.hole = hole
        self.time = time
        
    def __repr__(self):
        return f"Peg({self.hole},{self.time})"
    
    def __eq__(self, other):
        if not isinstance(other, Peg):
            return NotImplemented
        return self.hole == other.hole and self.time == other.time

class Jump:
    def __init__(self, start, over, end, time):
        self.start = start
        self.over = over
        self.end = end
        self.time = time
        
    def __repr__(self):
        return f"Jump({self.start},{self.over},{self.end},{self.time})"


def getPegIndex(peg, AllPegs):
    return AllPegs.index(peg) + Q + 1

def getJumpIndex(jump, AllJumps):
    return AllJumps.index(jump) + 1


def getPreconditionAxioms(AllJumps, AllPegs):
    for jump in AllJumps:
        clauses.append([-getJumpIndex(jump, AllJumps), getPegIndex(Peg(jump.start, jump.time), AllPegs)])
        clauses.append([-getJumpIndex(jump, AllJumps), getPegIndex(Peg(jump.over, jump.time), AllPegs)])
        clauses.append([-getJumpIndex(jump, AllJumps), -getPegIndex(Peg(jump.end, jump.time), AllPegs)])

def getCasualAxioms(AllJumps, AllPegs):
    for jump in AllJumps:
        clauses.append([-getJumpIndex(jump, AllJumps), -getPegIndex(Peg(jump.start, jump.time + 1), AllPegs)])
        clauses.append([-getJumpIndex(jump, AllJumps), -getPegIndex(Peg(jump.over, jump.time + 1), AllPegs)])
        clauses.append([-getJumpIndex(jump, AllJumps), getPegIndex(Peg(jump.end, jump.time + 1), AllPegs)])

def getFrameAxioms(AllJumps, AllPegs):
    for peg in AllPegs:
        validJumpsFromOrOver = []

        for jump in AllJumps:
            if (jump.start == peg.hole and jump.time == peg.time) or (jump.over == peg.hole and jump.time == peg.time):
                validJumpsFromOrOver.append(getJumpIndex(jump, AllJumps))
        
        if(Peg(peg.hole, peg.time + 1) in AllPegs):
            clauses.append([-getPegIndex(peg, AllPegs), getPegIndex(Peg(peg.hole, peg.time + 1), AllPegs), validJumpsFromOrOver])
    
    for peg in AllPegs:
        validJumpsInto = []
        for jump in AllJumps:
            if (jump.end == peg.hole and jump.time == peg.time):
                validJumpsInto.append(getJumpIndex(jump, AllJumps))
        
        if(Peg(peg.hole, peg.time + 1) in AllPegs):
            clauses.append([getPegIndex(peg, AllPegs), -getPegIndex(Peg(peg.hole, peg.time + 1), AllPegs), validJumpsInto])

def getOneActionAtATime(AllJumps):
    for jump in AllJumps:
        for j in AllJumps:
            indexOne = getJumpIndex(jump, AllJumps)
            indexTwo = getJumpIndex(j, AllJumps)
            if (jump != j) and (indexOne < indexTwo) and (jump.time == j.time):
                clauses.append([-indexOne, -indexTwo])
    
def getStartingState(AllPegs):
    for peg in AllPegs:
        if peg.time == 1:
            if AllPegs.index(peg) == 0:
                clauses.append([-getPegIndex(peg, AllPegs)])
            else:
                clauses.append([getPegIndex(peg, AllPegs)])

def getEndingState(AllPegs):
    for peg in AllPegs:
        for p in AllPegs:
            indexOne = getPegIndex(peg, AllPegs)
            indexTwo = getPegIndex(p, AllPegs)
            if (peg != p) and (indexOne < indexTwo) and (peg.time == N - 1) and (p.time == N - 1):
                clauses.append([-indexOne, -indexTwo])

inputTriples = []
initialTime = 0
N = 0
with open('Test', 'r') as file:
    c = 0
    for line in file:
        if c == 0:
            parts = line.split()
            N = int(parts[0])
            initialTime = parts[1]
            c += 1
            continue
        triple = tuple(map(int, line.split()))
        inputTriples.append(triple)

clauses = []
AllPegs = []
AllJumps = []

for i in range(1, N+1):
    for j in range(1, N):
        peg = Peg(i, j)
        AllPegs.append(peg)

for triple in inputTriples:
    A = triple[0]
    B = triple[1]
    C = triple[2]
    for i in range(1, N-1):
        AllJumps.append(Jump(A, B, C, i))
    for i in range(1, N-1):
        AllJumps.append(Jump(C, B, A, i))

P = len(AllPegs)
Q = len(AllJumps)

getPreconditionAxioms(AllJumps, AllPegs)
getCasualAxioms(AllJumps, AllPegs)
getFrameAxioms(AllJumps, AllPegs)
getOneActionAtATime(AllJumps)
getStartingState(AllPegs)
getEndingState(AllPegs)

#used to combine clauses like [23, -24, [1, 11]] into one array like [23, -24, 1, 11] for printing purposes
def combineList(clause):
    combinedClause = []
    for item in clause:
        if isinstance(item, list):
            combinedClause.extend(item)
        else:
            combinedClause.append(item)
    return combinedClause

with open('frontendOutput.txt', 'w') as file:
    for clause in clauses:
        combinedClause = combineList(clause)
        file.write(' '.join(map(str, combinedClause)) + '\n')
    file.write(str(0) + '\n')
    for jump in AllJumps:
        file.write(str(getJumpIndex(jump, AllJumps)) + ' ' + str(jump) + '\n')
    for peg in AllPegs:
        file.write(str(getPegIndex(peg, AllPegs)) + ' ' + str(peg) + '\n')
    
'''
The following test cases work (some of my outputs are not identical to the professors but when I play the peg game by hand, the solution is valid):
6 1
1 2 3
2 3 4
3 4 5
4 5 6
5 6 1
6 1 2

5 1
1 2 3
2 4 5

4 1
1 2 3
2 3 4
3 4 1
4 1 2

10 1
1 2 4
2 4 7
3 5 8
4 5 6
7 8 9
8 9 10
1 3 6
3 6 10
2 5 9
'''
