import operation


def process(s, d):
    opList = []
    stList = []

    def processLastOp():
        op = opList.pop()
        if op.arity == operation.UNARY:
            stList.append(op.method(stList.pop()))
        elif op.arity == operation.BINARY:
            b, a = stList.pop(), stList.pop()
            stList.append(op.method(a, b))

    curOpArity = operation.UNARY

    for t in s:
        if t == '(':
            opList.append('(')
            curOpArity = operation.UNARY
        elif t == ')':
            while opList[-1] != '(': processLastOp()
            opList.pop()
            curOpArity = operation.BINARY
        elif (t, curOpArity) in operation.opDict:
            curOp = operation.opDict[t, curOpArity]
            while len(opList) > 0 and opList[-1] != '(' and (
                    opList[-1].associativity == operation.LEFT and opList[-1].priority >= curOp.priority
                    or opList[-1].associativity == operation.RIGHT and opList[-1].priority > curOp.priority):
                processLastOp()
            opList.append(curOp)
            curOpArity = operation.UNARY
        else:
            stList.append(d[t])
            curOpArity = operation.BINARY

    while len(opList) > 0: processLastOp()

    return stList[-1]
