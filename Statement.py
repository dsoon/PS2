from abc import ABC
from Token import TokenType as TT

class Statement(ABC):
    valid_statements = [TT.DECLARE, TT.ASSIGN, TT.PRINT, TT.WHILE, TT.IF, TT.REPEAT, TT.CASE]

class DECL_Statement(Statement):
    def __init__(self, vname, vtype, line):
        assert vname != None and vtype != None and line != None, "DECL_Statement: None initialiser(s) found"

        self.vname = vname
        self.vtype = vtype
        self.line = line

class ARRAY_DECL_Statement(Statement):
    def __init__(self, vname, start, end, vtype, line):
        assert vname != None and start != None and end != None and vtype != None and line != None,"ARRAY_DECL_Statement: None initialiser(s) found"

        self.vname = vname
        self.start = start
        self.end = end
        self.vtype = vtype
        self.line = line

class ARRAY_ASSIGN_Statement(Statement):
    def __init__(self, vname, index, expr, line):
        assert vname != None and index != None and expr != None and line != None, "ARRAY_ASSIGN_Statement: None initialiser(s) found"

        self.vname = vname
        self.index = index
        self.expr = expr
        self.line = line

class ASSIGN_Statement(Statement):
    def __init__(self, vname, expr, line):
        assert vname != None and expr != None and line != None, "ASSIGN_Statement: None initialiser(s) found"

        self.vname = vname
        self.expr = expr
        self.line = line

class PRINT_Statement(Statement):
    def __init__(self, expr, line):
        assert expr != None and line != None, "PRINT_Statement: None initialiser(s) found"

        self.expr = expr
        self.line = line

class INPUT_Statement(Statement):
    def __init__(self, name, line):
        assert name != None and line != None, "INPUT_Statement: None initialiser(s) found"

        self.name = name
        self.line = line

class WHILE_Statement(Statement):
    def __init__(self, condition, statement_list, line):
        assert condition != None and statement_list != None and line != None, "WHILE_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.line = line

class REPEAT_Statement(Statement):
    def __init__(self, condition, statement_list, line):
        assert condition != None and statement_list != None and line != None, "REPEAT_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.line = line

class FOR_Statement(Statement):
    def __init__(self, assign, expr, step, statement_list, line):
        assert assign != None and expr!= None and statement_list != None and line != None, "FOR_Statement: None initialiser(s) found"

        self.assign = assign
        self.expr = expr
        self.step = step
        self.statement_list = statement_list
        self.line = line


class IF_Statement(Statement):
    def __init__(self, condition, statement_list, line):
        assert condition != None and statement_list != None and line != None, "IF_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.line = line

class IF_ELSE_Statement(Statement):
    def __init__(self, condition, statement_list, else_statement_list, line):
        assert condition != None and statement_list != None and else_statement_list != None and line != None, "IF_ELSE_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.else_statement_list = else_statement_list
        self.line = line


class CASE_Statement(Statement):
    def __init__(self):
        assert False, "CASE_Statement: Note implemented"

class FUNCTION_DECL_Statement(Statement):
    def __init__(self, name, args, statement_list, rtype, line):
        assert name != None and statement_list != None and rtype != None and line != None, "FUNCTION_DECL_Statement: None initialiser(s) found"

        # self.args can be None - this represents a procedure that takes no arguments

        self.name = name
        self.args = args
        self.stmt_list = statement_list
        self.rtype = rtype
        self.line = line

class PROC_DECL_Statement(Statement):
    def __init__(self, name, args, statement_list, line):
        assert name != None and statement_list != None and line != None, "PROC_DECL_Statement: None initialiser(s) found"

        # self.args can be None - this represents a procedure that takes no arguments

        self.name = name
        self.args = args
        self.statement_list = statement_list
        self.line = line

class PROC_Statement(Statement):
    def __init__(self, name, args, line):
        assert name != None and args != None and line != None, "PROC_Statement: None initialiser(s) found"

        self.name = name
        self.args = args
        self.line = line


class RETURN_Statement(Statement):
    def __init__(self, expr):

        assert expr != None, "RETURN_Statement expression is empty"

        self.expr = expr

class OPENFILE_Statement(Statement):
    def __init__(self, handle, mode, line):
        self.handle = handle
        self.mode = mode
        self.line = line

    def __str__(self):
        return f"OPENFILE_Statement: {self.handle} {self.mode} on line {self.line}"

class CLOSEFILE_Statement(Statement):
    def __init__(self, handle, line):
        self.handle = handle
        self.line = line

    def __str__(self):
        return f"CLOSEFILE_Statement: {self.handle} on line {self.line}"


class READFILE_Statement(Statement):
    def __init__(self, handle, variable, line):
        self.handle = handle
        self.variable = variable
        self.line = line

    def __str__(self):
        return f"READFILE_Statement: {self.handle} {self.variable} on line {self.line}"

class WRITEFILE_Statement(Statement):
    def __init__(self, handle, value, line):
        self.handle = handle
        self.value = value
        self.line = line

    def __str__(self):
        return f"WRITEFILE_Statement: {self.handle} {self.variable} on line {self.line}"
    

