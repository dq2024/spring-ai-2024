def deleteSingletonClause(clauses, assignments):
    singletonClauses = [c for c in clauses if len(c) == 1]

    while singletonClauses:
        unit = singletonClauses.pop()
        literal = unit[0]
        if literal > 0:
            assignments[abs(literal)] = True  
        else:
            assignments[abs(literal)] = False
            
        newClauses = []
        for clause in clauses:
            if literal not in clause:
                newClauses.append(clause)
        clauses = newClauses

        for clause in clauses:
            if -literal in clause:
                clause.remove(-literal)

        singletonClauses = []
        for clause in clauses:
            if len(clause) == 1:
                singletonClauses.append(clause)
    
    return clauses, assignments

def deletePureLiteral(clauses, assignments):
    literals = set()
    for clause in clauses:
        for literal in clause:
            literals.add(literal)

    pureLiterals = set()
    for literal in literals:
        if -literal not in literals:
            pureLiterals.add(literal)

    for l in pureLiterals:
        if l > 0:
            assignments[abs(l)] = True
        else:
            assignments[abs(l)] = False

    newClauses = []
    for clause in clauses:
        if not any(literal in pureLiterals for literal in clause):
            newClauses.append(clause)

    clauses = newClauses
    return clauses, assignments

def propagate(clauses, assignments, atom, truthValue):
    newClauses = []
    for clause in clauses:
        clauseSatisfied = False
        if atom in clause and truthValue:
            clauseSatisfied = True
        elif -atom in clause and not truthValue:
            clauseSatisfied = True
        
        if clauseSatisfied:
            continue  
        
        newClause = []
        for literal in clause:
            if literal != atom and literal != -atom:
                newClause.append(literal)
        newClauses.append(newClause)
    
    assignments[atom] = truthValue
    return newClauses, assignments

def getUnboundAtom(assignments, count):
    for i in range(1, count + 1):
        if (i not in assignments) and (-i not in assignments):
            return i
    return None

def DPLL(clauses, assignments, backMatters):
    # remove singleton clauses
    clauses, assignments = deleteSingletonClause(clauses, assignments)
    # remove pure literals
    clauses, assignments = deletePureLiteral(clauses, assignments)

    if not clauses:
        return assignments
    
    for clause in clauses:
        if len(clause) == 0:
            return "NO SOLUTION"
    
    unboundAtom = getUnboundAtom(assignments, max(backMatters.keys()))
    if unboundAtom is None:
        return assignments
    
    for truthValue in [True, False]:
        newAssignments = assignments.copy()
        newAssignments[unboundAtom] = truthValue
        newClauses, updatedAssignments = propagate(clauses, newAssignments, unboundAtom, truthValue)
        result = DPLL(newClauses, updatedAssignments, backMatters)
        if result != "NO SOLUTION":
            return result

    return "NO SOLUTION"

def main():
    with open('frontendOutput.txt', 'r') as file:
        clauses = []
        backMatters = {}

        for line in file:
            newLine = line.strip()
            if newLine == '0':
                break 

            parts = newLine.split()
            clause = [int(part) for part in parts]
            if clause:
                clauses.append(clause)

        for line in file: 
            newLine = line.strip()
            parts = newLine.split(' ', 1)
            if len(parts) == 2:
                backMatter, description = parts
                backMatters[int(backMatter)] = description

        assignments = {}
        result = DPLL(clauses, assignments, backMatters)

    with open('DPLLoutput.txt', 'w') as file:
        if result == "NO SOLUTION":
            file.write("0\n")
            for i, j in sorted(backMatters.items()):
                    file.write(f"{i} {j}\n")
        else:
            for atom in sorted(assignments.keys()):
                if atom not in result:
                    result[atom] = True

            for res in sorted(result.keys()):
                if result[res]:
                    file.write(f"{res} {'T'}\n")
                else:
                    file.write(f"{res} {'F'}\n")
            file.write("0\n")

            for i, j in sorted(backMatters.items()):
                file.write(f"{i} {j}\n")
main()