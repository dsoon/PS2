import abc
import utilities as util

from environment import Environment as environ
from environment import Symbol, Array_Symbol, Function_Symbol, File_Symbol
from token import TokenType as TT, Token


class Statement ( abc.ABC ):

    valid_statements = [
        TT.CONSTANT,
        TT.DECLARE,
        TT.TYPE,
        TT.CLASS,
        TT.PRIVATE,
        TT.PUBLIC,
        TT.FUNCTION,
        TT.RETURN,
        TT.PROCEDURE,
        TT.CALL,
        TT.PRINT,
        TT.OUTPUT,
        TT.INPUT,
        TT.OPENFILE,
        TT.CLOSEFILE,
        TT.READFILE,
        TT.WRITEFILE,
        TT.WHILE,
        TT.REPEAT,
        TT.FOR,
        TT.IF,
        TT.CASE
    ]

    @abc.abstractmethod # each statement implements this methid, which us called by the Interpretor
    def interpret(self):
        pass

class DECLARE ( Statement ):

    def __init__(self, vname, vtype, line):
        assert vname != None and vtype != None and line != None, \
            "DECLARE statement: None initialiser(s) found"

        self.vname = vname
        self.vtype = vtype
        self.line = line

    def interpret(self):

        symbol = Symbol(self.vname, self.vtype)
        environ.add_variable(symbol)


class DECLARE_ARRAY ( Statement ):

    def __init__(self, vname, start, end, vtype, line):
        assert vname != None and start != None and end != None and vtype != None and line != None,\
            "ARRAY DECLARATION statement: None initialiser(s) found"

        self.vname = vname
        self.vtype = vtype

        self.start = start
        self.end = end
        self.line = line

    def interpret(self):

        start = self.start.evaluate()
        end =   self.end.evaluate()
                        
        if start > end or start < 0:
            raise RuntimeError([self.line, f"ARRAY declaration start index > end index or start index < 0"])

        symbol = Array_Symbol(self.vname, self.vtype, start, end)
        environ.add_variable(symbol)


class ARRAY_ASSIGN ( Statement ):

    def __init__(self, vname, index, expr, line):
        assert vname != None and index != None and expr != None and line != None, \
            "ARRAY ASSIGN statement: None initialiser(s) found"

        self.vname = vname
        self.index = index
        self.expr = expr
        self.line = line

    def interpret(self):

        index = self.index.evaluate()
        expr  = self.expr.evaluate()

        symbol = environ.get_variable(self.vname)

        if not isinstance(symbol, Array_Symbol):
            raise RuntimeError([self.line, f"symbol {self.vname} is not an array"])

        if index >= symbol.s_idx and index <= symbol.e_idx:
            symbol.value[index-1] = expr
        else:
            raise RuntimeError([self.line, f"{symbol.vname}[{index}], index out of range"])

class ASSIGN ( Statement ):

    def __init__(self, vname, expr, line):
        assert vname != None and expr != None and line != None, \
            "ASSIGN statement: None initialiser(s) found"

        self.vname = vname
        self.expr = expr
        self.line = line

    def interpret(self):
        value  = self.expr.evaluate()

        symbol = environ.get_variable(self.vname)
        symbol.value = value


class PRINT ( Statement ):

    def __init__(self, exprlist, line):
        assert exprlist != None and line != None, "PRINT_Statement: None initialiser(s) found"

        self.exprlist = exprlist
        self.line = line

    def interpret(self):

        for expr in self.exprlist:

            value = expr.evaluate()

            if value == None:
                raise RuntimeError([self.line, "No expression to print"])

            if type(value) is bool: # Ensure Python True and False are in uppercase 
                value = str(value).upper()

            print (value, end="") 
            
        print()

class INPUT ( Statement ):

    def __init__(self, name, line):
        assert name != None and line != None, \
            "INPUT statement: None initialiser(s) found"

        self.name = name
        self.line = line

    def interpret(self):

        symbol = environ.get_variable(self.name)

        vtype = symbol.vtype
        value = input()

        if vtype.type == TT.INTEGER:
            symbol.value = int(value)

        elif vtype.type == TT.REAL:
            symbol.value = float(value)

        elif vtype == TT.BOOLEAN:
            symbol.value = bool(value.capitalize())

        elif vtype == TT.STRING or TT.CHAR:
            symbol.value = value
        else:
            raise RuntimeError([self.line, f"INPUT() does not recognise the data type of {self.name}"])


class WHILE ( Statement ):

    def __init__(self, condition, statement_list, line):
        assert condition != None and statement_list != None and line != None, "WHILE_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.line = line


    def interpret(self):
        
        environ.push(environ()) # push new scope to stack
        
        while self.condition.evaluate() == True:

            for stmt in self.statement_list:
                stmt.interpret()

        environ.pop() # pop scope


class REPEAT ( Statement ):
    def __init__(self, condition, statement_list, line):
        assert condition != None and statement_list != None and line != None, "REPEAT_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.line = line

    def interpret(self):

        environ.push(environ()) # push new scope to stack
        
        while True:
            for stmt in self.statement_list:
                stmt.interpret()

            if self.condition.evaluate() == True:
                break
                
        environ.pop() # pop scope


class FOR ( Statement ):
    def __init__(self, assign, expr, step, statement_list, line):
        assert assign != None and expr!= None and statement_list != None and line != None, "FOR_Statement: None initialiser(s) found"

        self.assign = assign
        self.expr = expr
        self.step = step
        self.statement_list = statement_list
        self.line = line

    def interpret(self):

        ####
        # Declare a loop variable, normally all variable are explicitly declared, except for loop variables. 
    
        environ.push(environ()) # push new scope to stack

        symbol = Symbol(self.assign.vname, Token(TT.INTEGER, "", self.assign.vname, self.assign.line))

        environ.add_variable( symbol )

        ####
        # The assign node holds the starting value and the statement expr holds the end value
        # The end value is inclusive in pseudocode, hence we need to add 1
        # Create a range iterator for the FOR loop depending is a step is defined


        r = range(self.assign.expr.evaluate(), self.expr.evaluate() + 1)

        if self.step != None:
            r = range(self.assign.expr.evaluate(), self.expr.evaluate() + 1, self.step.evaluate())

        symbol = environ.get_variable(self.assign.vname)

        for i in r:

            # On each iteration we set the loop variable
            symbol.value = i

            # Now execute the for loop statement block
            for stmt in self.statement_list:
                stmt.interpret()

        environ.pop() # pop scope



class IF ( Statement ):
    def __init__(self, condition, statement_list, line):
        assert condition != None and statement_list != None and line != None, "IF_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.line = line

    def interpret(self):

        if self.condition.evaluate() == True:
            environ.push(environ()) # push new scope to stack

            for stmt in self.statement_list:
                stmt.interpret()
            
            environ.pop() # pop scope



class IF_ELSE ( Statement ):

    def __init__(self, condition, statement_list, else_statement_list, line):
        assert condition != None and statement_list != None and else_statement_list != None and line != None, "IF_ELSE_Statement: None initialiser(s) found"

        self.condition = condition
        self.statement_list = statement_list
        self.else_statement_list = else_statement_list
        self.line = line

    def interpret(self):

        if self.condition.evaluate() == True:

            environ.push(environ()) # push new scope to stack

            for stmt in self.statement_list:
                stmt.interpret()

            environ.pop() # pop scope
        
        else:

            environ.push(environ()) # push new scope to stack

            for stmt in self.else_statement_list:
                stmt.interpret()

            environ.pop() # pop scope


class CASE ( Statement ):

    def __init__(self):
        assert False, "CASE_Statement: Note implemented"

class DECLARE_FUNCTION ( Statement ):

    def __init__(self, name, args, statement_list, rtype, line):
        assert name != None and statement_list != None and rtype != None and line != None, \
            "FUNCTION_DECLARATION statement: None initialiser(s) found"

        # self.args can be None - this represents a procedure that takes no arguments

        self.name = name
        self.args = args
        self.stmt_list = statement_list
        self.rtype = rtype
        self.line = line

    def interpret(self):

        symbol = Function_Symbol(self.name, self.args, self.rtype, self.stmt_list, self.line)
        environ.add_variable(symbol)


class PROCEDURE_DECLARATION ( Statement ):
    def __init__(self, name, args, statement_list, line):
        assert name != None and statement_list != None and line != None, "PROC_DECL_Statement: None initialiser(s) found"

        # self.args can be None - this represents a procedure that takes no arguments

        self.name = name
        self.args = args
        self.statement_list = statement_list
        self.line = line

class CALL ( Statement ):

    def __init__(self, name, args, line):
        assert name != None and args != None and line != None, "CALL statement: None initialiser(s) found"

        self.name = name
        self.args = args
        self.line = line

    def interpret(self):

        if self.name == "DEBUG":

            if len(self.args) != 0:
                arg = self.args[0].evaluate()

            if arg == "globals":
                environ.dump_global_variables()

            else:
                raise RuntimeError([self.line, f"Unrecognised DEBUG parameter {arg}"])
        
        else:
            raise RuntimeError([self.line, f"Unrecognised procedure call '{self.name}'"])


class RETURN ( Statement ):

    def __init__(self, expr):

        assert expr != None, "RETURN_Statement expression is empty"

        self.expr = expr

    def interpret(self):
        
        # Use Python's exception mechanism to return from calling procedure / function
        expr = None
        if self.expr != None:
            expr = self.expr.evaluate()
            
        raise util.Return(expr)


class OPENFILE( Statement ):
    def __init__(self, handle, mode, line):
        self.handle = handle
        self.mode = mode
        self.line = line

    def interpret(self):

        name = self.handle.evaluate()

        mode = None
        if self.mode == TT.READ:
            mode = "r"

        elif self.mode == TT.WRITE:
            mode = "w"

        elif self.mode == TT.APPEND:
            mode = "a"

        else:
            raise RuntimeError([self.line, f"OPENFILE - unrecognised mode '{self.mode}'"])

        try:
            file_id = open(name, mode)
        except Exception as e:
            raise RuntimeError([self.line, f"unexpected error while executing OPENFILE {e}"])

        environ.add_variable(File_Symbol(name, mode,file_id))


    def __str__(self):
        return f"OPENFILE statement: {self.handle} {self.mode} on line {self.line}"

class CLOSEFILE ( Statement ):
    def __init__(self, handle, line):
        self.handle = handle
        self.line = line

    def __str__(self):
        return f"CLOSEFILE statement: {self.handle} on line {self.line}"

    def interpret(self):

        name = self.handle.evaluate()

        handle = environ.get_variable(name)

        try:
            handle._fileid.close()

        except Exception as e:
            raise RuntimeError([self.line, f"unexpected error while executing CLOSEFILE {e}"])

        environ.remove_variable(handle.vname)

class READFILE ( Statement ):
    def __init__(self, handle, variable, line):
        self.handle = handle
        self.variable = variable
        self.line = line

    def __str__(self):
        return f"READFILE statement: {self.handle} {self.variable} on line {self.line}"


    def interpret(self):

        name = self.handle.evaluate()

        symbol = environ.get_variable(name)

        handle = symbol._fileid

        variable = environ.get_variable(self.variable) 

        try:
            line = handle.readline()

            variable.value = line.strip()

        except Exception as e:
            raise RuntimeError([self.line, f"unexpected error while executing READFILE {e}"])


class WRITEFILE ( Statement ):

    def __init__(self, handle, value, line):
        self.handle = handle
        self.value = value
        self.line = line

    def __str__(self):
        return f"WRITEFILE statement: {self.handle} {self.variable} on line {self.line}"
    

    def interpret(self):

        name = self.handle.evaluate()

        symbol = environ.get_variable(name)
        
        handle = symbol._fileid

        value = self.value.evaluate() 

        try:

            handle.writelines([str(value)+"\n"])

        except Exception as e:
            raise RuntimeError([self.line, f"unexpected error while executing WRITEFILE {e}"])

