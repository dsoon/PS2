from abc import ABC

class Expr(ABC):
    pass

class UNARY_Expr(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class BINARY_Expr(Expr):
    def __init__(self, left, operator, right, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line

class LITERAL_Expr(Expr):
    def __init__(self, expression):
        self.expression = expression

class GROUPING_Expr(Expr):
    def __init__(self, expression):
        self.expression = expression

class IDENTIFIER_Expr(Expr):
    def __init__(self, name):
        self.name = name

class FUNCTION_Expr(Expr):
    def __init__(self, name, args, line):
        self.name = name
        self.args = args
        self.line = line

class ARRAY_Expr(Expr):
    def __init__(self, name, index, line):
        self.name = name
        self.index = index
        self.line = line