UNARY = 1
BINARY = 2
LEFT = 1
RIGHT = 2


class Operation:
    def __init__(self, name, arity, associativity, priority, method):
        self.name = name
        self.arity = arity
        self.associativity = associativity
        self.priority = priority
        self.method = method

    def __repr__(self):
        return ("UNARY" if self.arity == UNARY else "BINARY") + self.name


opDict = dict()

opDict['+', UNARY] = Operation('+', UNARY, RIGHT, 3, lambda a: +a)
opDict['-', UNARY] = Operation('-', UNARY, RIGHT, 3, lambda a: -a)
opDict['+', BINARY] = Operation('+', BINARY, LEFT, 1, lambda a, b: a + b)
opDict['-', BINARY] = Operation('-', BINARY, LEFT, 1, lambda a, b: a - b)
opDict['*', BINARY] = Operation('*', BINARY, LEFT, 2, lambda a, b: a * b)
opDict['/', BINARY] = Operation('/', BINARY, LEFT, 2, lambda a, b: a / b)
opDict['^', BINARY] = Operation('^', BINARY, RIGHT, 3, lambda a, b: a ** b)
