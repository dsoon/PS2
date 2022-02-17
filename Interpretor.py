from Token import TokenType as TT, Token
from Statement import PRINT_Statement as PS, IF_Statement as IS, IF_ELSE_Statement as IES, WHILE_Statement as WS, DECL_Statement as DS, \
                      ARRAY_DECL_Statement as ADS, ASSIGN_Statement as AS, ARRAY_ASSIGN_Statement as AAS,REPEAT_Statement as RS, FOR_Statement as FS, \
                      INPUT_Statement as IPS, PROC_Statement as PRS, \
                      FUNCTION_DECL_Statement as FDS, RETURN_Statement as RST

import Expression

from Environment import Environment as environ, Symbol as Sym, Array_Symbol as ASym, Function_Symbol as FSym, Return_Symbol as RtnSym

import Utilities as util

class Interpretor:

    def __init__(self, stmt_list):
        self.stmt_list = stmt_list

    def interpret(self):

        if self.stmt_list != None:

            for stmt in self.stmt_list:
                
                try:
                    if isinstance(stmt, PS): # Print statement

                        for expr in stmt.expr:

                            expr = self.visitNode(expr)

                            if expr == None:
                                raise RuntimeError([stmt.line, "No expression to print"])

                            if type(expr) is bool: # Ensure Python True and False are in uppercase 
                                expr = str(expr).upper()

                            print (expr, end="") 
                            
                        print()

                    elif isinstance(stmt, IPS): # Input statement

                        symbol = environ.get_variable(stmt.name) 
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
                            raise RuntimeError([stmt.line, f"INPUT() does not recognise the data type of {stmt.name}"])

                    elif isinstance(stmt, IS): # If statement
                        if self.visitNode(stmt.condition):
                            environ.push(environ()) # push new scope to stack
                            Interpretor(stmt.statement_list).interpret()
                            environ.pop() # pop scope

                    elif isinstance(stmt, IES): # If else statement
                        if self.visitNode(stmt.condition):
                            environ.push(environ()) # push new scope to stack
                            Interpretor(stmt.statement_list).interpret()
                            environ.pop() # pop scope
                        else:
                            environ.push(environ()) # push new scope to stack
                            Interpretor(stmt.else_statement_list).interpret()
                            environ.pop() # pop scope

                    elif isinstance(stmt, WS): # While statement
                        environ.push(environ()) # push new scope to stack
                        while self.visitNode(stmt.condition):
                            Interpretor(stmt.statement_list).interpret()
                        environ.pop() # pop scope

                    elif isinstance(stmt, RS): # Repeat statement
                        environ.push(environ()) # push new scope to stack
                        while True:
                            Interpretor(stmt.statement_list).interpret()
                            if self.visitNode(stmt.condition):
                                break
                        environ.pop() # pop scope

                    elif isinstance(stmt, FS): # For statement

                        ####
                        # Declare a loop variable, normally all variable are explicitly declared, except for loop variables. 
                        environ.push(environ()) # push new scope to stack

                        symbol = Sym(stmt.assign.vname, Token(TT.INTEGER,"", stmt.assign.vname, stmt.assign.line))

                        environ.add_variable( symbol )

                        ####

                        # The assign node holds the starting value and the statement expr holds the end value
                        # The end value is inclusive in pseudocode, hence we need to add 1
                        # Create a range iterator for the FOR loop depending is a step is defined
                        r = range(self.visitNode(stmt.assign.expr), self.visitNode(stmt.expr) + 1)
                        if stmt.step != None:
                            r = range(self.visitNode(stmt.assign.expr), self.visitNode(stmt.expr) + 1, self.visitNode(stmt.step))

                        symbol = environ.get_variable(stmt.assign.vname)

                        for i in r:

                            # On each iteration we set the loop variable
                            symbol.value = i

                            # Now execute the for loop statement block
                            Interpretor(stmt.statement_list).interpret()
                        environ.pop() # pop scope

                    elif isinstance(stmt, DS): # Declaration
                        name = stmt.vname
                        vtype = stmt.vtype

                        symbol = Sym(name, vtype)
                        environ.add_variable(symbol)

                    elif isinstance(stmt, FDS): # Function Declaration
                        
                        symbol = FSym(stmt.name, stmt.args, stmt.rtype, stmt.stmt_list,stmt.line)
                        environ.add_variable(symbol)

                    elif isinstance(stmt, ADS): # Declaration
                        name = stmt.vname
                        vtype = stmt.vtype

                        start = self.visitNode(stmt.start)
                        end = self.visitNode(stmt.end)
                        
                        if start > end or start < 0:
                            raise RuntimeError([stmt.line, f"ARRAY declaration start index > end index or start index < 0"])

                        symbol = ASym(name, vtype, start, end)
                        environ.add_variable(symbol)

                    elif isinstance(stmt, AS): # Assignment
                        name = stmt.vname
                        value  = self.visitNode(stmt.expr)

                        symbol = environ.get_variable(name)
                        symbol.value = value

                    elif isinstance(stmt, AAS): # Array Assignment
                        name = stmt.vname
                        index = self.visitNode(stmt.index)
                        expr = self.visitNode(stmt.expr)

                        symbol = environ.get_variable(name)

                        if index >= symbol.s_idx and index <= symbol.e_idx:
                            symbol.value[index-1] = expr
                        else:
                            raise RuntimeError([stmt.line, f"{symbol.vname}[{index}], index out of range"])

                    elif isinstance(stmt, PRS): # Procedure call
                        name = stmt.name
                        if name == "DEBUG":
                            arg = self.visitNode(stmt.args[0])
                            if arg == "globals":
                                environ.dump_global_variables()
                            else:
                                raise RuntimeError([stmt.line, f"Unrecognised DEBUG parameter {arg}"])

                    elif isinstance(stmt, RST): # Return statement from function
                        raise util.Return(self.visitNode(stmt.expr))

                except NameError as ne:
                    raise RuntimeError([stmt.line, f"{ne}"])
    
    def visitNode(self, expr):

        if isinstance(expr, Expression.LITERAL_Expr): # Reached the leaves
            return expr.expression

        if isinstance(expr, Expression.IDENTIFIER_Expr): # Reached the leaves
            name = expr.name
            return environ.get_variable(name).value

        elif isinstance(expr, Expression.BINARY_Expr): # Post-order tree traversal 

            left  = self.visitNode(expr.left)
            right = self.visitNode(expr.right)

            op = expr.operator.type

            # check to ensure both left and right are not None
            if left == None or right == None:
                raise RuntimeError([expr.operator.line, f"the left or the right expression of the {expr.operator.lexeme} operator is empty"])

            # check for valid number operations 
            if util.isNumber(left) and not util.isNumber(right) or not util.isNumber(left) and util.isNumber(right):
                raise RuntimeError([expr.operator.line, f"type mismatch on operator '{expr.operator.lexeme}', both expressions need to be numbers"])

            # check for valid string operations
            if util.isString(left) and util.isString(right) and op in [TT.PLUS, TT.MINUS, TT.STAR, TT.SLASH, TT.DIV, TT.MOD]:
                raise RuntimeError([expr.operator.line, f"invalid string operator '{expr.operator.lexeme}'"])
            
            if  op == TT.PLUS:
                return left + right

            elif op  == TT.AMPERSAND:
                # Check that both left and right are of type STRING
                if type(left) is str and type(right) is str:
                    return left + right
                else:
                    raise RuntimeError([expr.operator.line, f"String concatenation '&' operates on STRINGs only"])

            elif op  == TT.MINUS:
                return left - right

            elif op  == TT.STAR:
                return left * right

            elif op  == TT.SLASH:
                return left / right

            elif op == TT.AND:
                return left and right

            elif op == TT.OR:
                return left or right

            elif op  == TT.DIV:
                if util.isNumber(left) and util.isNumber(right):
                    return left // right
                else:
                    raise RuntimeError([expr.operator.line, f"DIV operates on numbers ONLY"])

            elif op  == TT.MOD:
                if util.isNumber(left) and util.isNumber(right):
                    return left % right
                else:
                    raise RuntimeError([expr.operator.line, f"MOD operates on numbers ONLY"])

            elif op  == TT.GREATER_EQUAL:
                return left >= right

            elif op  == TT.GREATER:
                return left > right

            elif op  == TT.LESS:
                return left < right

            elif op  == TT.LESS_EQUAL:
                return left <= right

            elif op  == TT.EQUAL:
                return left == right

            elif op  == TT.LESS_GREATER:
                return left != right

            elif op  == TT.BANG_EQUAL:
                return left != right

            else:
                raise RuntimeError([expr.operator.line, f"Unecognised binary operator '{expr.operator.lexeme}'"])

        elif isinstance(expr, Expression.GROUPING_Expr):
            return self.visitNode(expr.expression)

        elif isinstance(expr, Expression.UNARY_Expr):
            right  = self.visitNode(expr.right)
            if expr.operator.lexeme == '-':
                return -right

        elif isinstance(expr, Expression.ARRAY_Expr):

            name = expr.name
            index = self.visitNode(expr.index)
            symbol = environ.get_variable(name)

            if index < symbol.s_idx or index > symbol.e_idx:
                raise RuntimeError([expr.line, f"Array index {index} out of range"])
            elif symbol.value[index-symbol.s_idx] == None:
                raise RuntimeError([expr.line, f"Array index {name}[{index}] not set"])

            return symbol.value[index-symbol.s_idx]

        elif isinstance(expr, Expression.FUNCTION_Expr):

            # Check if any internal functions match
            if expr.name == "INT":
                if len(expr.args) != 1:
                    raise RuntimeError([expr.line, f"INT() requires 1 argument, it received {len(expr.args)}"])

                val = self.visitNode(expr.args[0])
                if not (type (val) == int or type(val) == float):
                    raise RuntimeError([expr.line, f"INT() requires a an INTEGER or REAL argument"])

                return int(val)

            elif expr.name == "RAND":
                if len(expr.args) != 2:
                    raise RuntimeError([expr.line, f"RAND() requires 2 arguments, it received {len(expr.args)}"])

                from random import randint
                start = self.visitNode(expr.args[0])
                end   = self.visitNode(expr.args[1])

                if type(start) == int and type(end) == int:
                    return randint(self.visitNode(expr.args[0]), self.visitNode(expr.args[1]))
                else:
                    raise RuntimeError([expr.line, f"RAND() requires 2 integer arguments"])

            elif expr.name == "RIGHT":
                if len(expr.args) != 2:
                    raise RuntimeError([expr.line, f"RIGHT() requires 2 arguments, it received {len(expr.args)}"])
                this_string = self.visitNode(expr.args[0])

                # Check that this is a string
                if type(this_string) != str:
                    raise RuntimeError([expr.line, f"RIGHT() requires a STRING, not '{this_string}'"])    

                x = self.visitNode(expr.args[1])
                if type(x) != int:
                    raise RuntimeError([expr.line, f"RIGHT() requires an INTEGER length, not '{x}'"])    

                return this_string[-x:]

            elif expr.name == "LENGTH":
                if len(expr.args) != 1:
                    raise RuntimeError([expr.line, f"LENGTH() function requires 2 arguments, it received {len(expr.args)}"])
                this_string = self.visitNode(expr.args[0])

                # Check that this is a string
                if type(this_string) != str:
                    raise RuntimeError([expr.line, f"LENGTH() requires a STRING, not '{this_string}'"])    

                return len(this_string)

            elif expr.name == "MID":
                if len(expr.args) != 3:
                    raise RuntimeError([expr.line, f"MID() requires 3 arguments, it received {len(expr.args)}"])

                this_string = self.visitNode(expr.args[0])

                # Check that this is a string
                if type(this_string) != str:
                    raise RuntimeError([expr.line, f"MID() requires a STRING, not '{this_string}'"])    

                start = self.visitNode(expr.args[1])
                x     = self.visitNode(expr.args[2])

                if type(start) == int and type(x) == int:

                    # Ensure start and x are valid
                    if start > 0 and start + x <= len(this_string):
                        return this_string[start-1:start+x]
                    else:
                        RuntimeError([expr.line, f"MID() arguments are invalid. Ensure start index > 0, start + x <= LENGTH(the_string)"])
                else:
                    raise RuntimeError([expr.line, f"MID() requires 2 integer arguments"])

            elif expr.name == "UCASE":
                    if len(expr.args) != 1:
                        raise RuntimeError([expr.line, f"UCASE() function requires 1 argument, it received {len(expr.args)}"])

                    char  = self.visitNode(expr.args[0])
                    if not util.isChar(char):
                        raise RuntimeError([expr.line, f"UCASE() argument should be of type CHAR"])

                    return char.upper()

            elif expr.name == "LCASE":
                    if len(expr.args) != 1:
                        raise RuntimeError([expr.line, f"LCASE() function requires 1 argument, it received {len(expr.args)}"])

                    char  = self.visitNode(expr.args[0])
                    if not util.isChar(char):
                        raise RuntimeError([expr.line, f"LCASE() argument should be of type CHAR"])

                    return char.lower()


            elif expr.name == "DEBUG":

                if len(expr.args) != 1:
                    raise RuntimeError([expr.line, f"DEBUG() function requires 1 argument, it received {len(expr.args)}"])

                command  = self.visitNode(expr.args[0])
                if command.upper() == "DUMP GLOBALS":
                    environ.dump_global_variables()
                
            elif environ.symbol_defined(expr.name): # Check if this is a user defined function
                symbol = environ.get_variable(expr.name)

                environ.push(environ())

                for i, s in enumerate(symbol.args):
                    id_name = symbol.args[i][0]
                    id_type = symbol.args[i][1]
                    environ.add_variable(Sym(id_name, id_type ,self.visitNode(expr.args[i])))
                try:
                    return_val = None
                    Interpretor(symbol.stmt_list).interpret()
                except util.Return as r:
                    return_val = r.args[0]
                environ.pop()

                if return_val == None:
                    raise RuntimeError([symbol.line, f"Function '{expr.name}()' returned without a value"])

                return return_val
            
            else:
                raise RuntimeError([expr.line, f"Unecognised internal function '{expr.name}()'"])


            