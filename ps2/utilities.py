def isNumber(expr):
    return type (expr) in [int, float]

def isString(expr):
    return type (expr) in [str]

def isChar(expr):
    return type (expr) in [str] and len(expr) == 1

def isBoolean(expr):
    return type (expr) in [bool]

class Return(Exception):
    pass