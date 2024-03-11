with open("DPLLoutput.txt", 'r') as file:
    lines = file.readlines()

    zeroIndex = lines.index('0\n')
    assignmentLines = lines[:zeroIndex]
    jumpLines = lines[zeroIndex + 1:]

    assignments = {}
    for line in assignmentLines:
        var, val = line.strip().split()
        assignments[int(var)] = val == 'T'

    if not assignments:
        print("NO SOLUTION")
        quit

    jumps = []
    for line in jumpLines:
        id, atom = line.strip().split(' ', 1)
        if "Jump" in atom and assignments.get(int(id), False):
            # https://www.w3schools.com/python/ref_string_rfind.asp
            time = int(atom[atom.rfind(',')+1:atom.rfind(')')])
            jumps.append((time, atom))
    
    for time, atom in sorted(jumps):
        print(atom)