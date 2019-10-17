# Prolog compiler in Python

import json

terms = set()
predicates = set()
facts = list()
marked = set()

def JSON2base(fileName):
    src = json.load(open(fileName))
    terms = set(src["station"])
    log = "Terms:\n" + ", ".join(terms) + "\n\nFacts:\n"

    for i in range(len(src["station"])):
        paths = list(filter(lambda j: (src["link"][i][j] > 0) and (j > i), range(len(src["link"][i]))))
        for path in paths:
            factExpr = "link(" + src["station"][i] + ", " + src["station"][path] + ")"
            log += factExpr + "\n" 
            getFact(factExpr)

    for station in src["pausing"]:
        factExpr = "pausing(" + station + ")"
        log += factExpr + "\n" 
        getFact(factExpr)

    return log

def getFact(factExpr):     # <rule-name>(term, ...)
    factName = factExpr[:-1].split('(')[0].strip()
    factArgs = [arg.strip() for arg in factExpr[:-1].split('(')[1].split(',')]
    facts.append([factName, factArgs])

    terms.update(factArgs)              # Same as this: terms |= set(factArgs)
    predicates.update([factName])

# Need develop it
def getRule(ruleExpr):
    predicate = ruleExpr.split(':-')[0]
    body = ruleExpr.split(':-')[1]
    rules.append({predicate: body})
    pass

def saveProblem(solution, fileName='pylog'):
    with open(fileName, 'w') as fs:
        fs.write(solution)

# Rules (max = 5, total: 4)
ruleExpr = [
    "link(X, X) :- !",
    "link(X, Y) :-  link(X, Z) and link(Z, Y) \
                    and not pausing(Z)        \
                    and not pausing(X)        \
                    and not pausing(Y)",
    "link(X, Y) :-  link(Y, X)",
    "link(X, Y, Z) :- link(X, Y) and link(Y, Z)"
]

# Maximum recursion depth 
# MAX_DEPTH = 5

# Template
# def __call(predicate, arguments):
#     return [predicate, arguments] in facts

def pausing(station):
    return ['pausing', [station]] in facts

# Already contain rules R3
def link(X, Y):
    return not pausing(X)               \
       and not pausing(Y)               \
       and (['link', [X, Y]] in facts   \
         or ['link', [Y, X]] in facts)  # R3

def R1(x, y):
    return x == y

def R2(x, y):
    if R1(x, y):        # Goal
        return True
    
    marked.update([x])
    queue = list(filter(lambda z: z not in marked and link(x, z), terms))
    
    # Version 1
    # while queue:
    #     z = queue.pop(0)
    #     newGoal = R2(z, y)
    #     if not newGoal:
    #         marked.remove(z)
    #     else:
    #         return newGoal

    # Version 2
    goal = False
    while queue:
        z = queue.pop(0)
        goal = goal or R2(z, y)
    
    return goal

def R4(x, y, z):
    __xy = R2(x, y)
    if __xy:
        marked.clear()
        return R2(y, z)
    return False

def process(predicate, arguments):
    argc = len(arguments)
    if argc in range(1, 4):
        if len(arguments) == 1:
            return predicate == 'pausing' and pausing(arguments)
        elif len(arguments) == 2:
                return R2(arguments[0], arguments[1])
        else:
            return R4(arguments[0], arguments[1], arguments[2])
    return False

def goal(expr, recursionFlag=False):
    exprName = expr[:-1].split('(')[0].strip()
    exprArgs = [arg.strip() for arg in expr[:-1].split('(')[1].split(',')]

    # Check existance of predicate
    if exprName in predicates:
        # Check existance of arguments in our knowledge base
        if set(exprArgs).issubset(terms):   # Same as this: set(exprArgs) <= terms
            # Check existance of facts and solve our goal
            marked.clear()
            return process(exprName, exprArgs)

    return False

if __name__ == "__main__":
    try:
        import sys
        log = JSON2base(sys.argv[1])
        ruleExpr = [' '.join(r.split()) for r in ruleExpr]  # modified rules: cut off space symbols
        rules = "\nRules:\n" + "\n".join(ruleExpr)
        
        goalExpr = str(input("Input GOAL: "))
        question = "\n\nGoal:\n" + goalExpr
        answer = goal(goalExpr)

        solution = log + rules + question + "\n" + str(answer)
        saveProblem(solution)

        print(answer)
    except IndexError:
        print('Command line: python <source> <fileName>')