from token import TokenType as TT
from expression import LITERAL, IDENTIFIER, ARRAY, BINARY, UNARY, FUNCTION, GROUPING
from statement import Statement, DECLARE, ASSIGN, DECLARE_ARRAY, DECLARE_FUNCTION, ARRAY_ASSIGN, PRINT, INPUT, IF, IF_ELSE, WHILE, REPEAT, FOR, CALL, OPENFILE, CLOSEFILE, READFILE, WRITEFILE, RETURN

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        if self.current < len(self.tokens):
            tok = self.tokens[self.current]
            self.current += 1
            return tok
        else:
            raise SyntaxError([self.tokens[self.current].line, "Unexpected EOF"])

    def undo(self):
        if self.current > 0:
            self.current -= 1

    def sync(self, *argv):
        while self.peek().type != TT.AT_EOF and self.peek().type not in Statement.valid_statements:
            self.advance() # throw away tokens

    def previous(self):
        if self.current > 0:
            return self.tokens[self.current - 1]
        else:
            raise RuntimeError([self.tokens[self.current].line, "Internal: Call to Parser.previous without previous token"])

    def isAtEnd(self):
        return self.peek().type == TT.AT_EOF            

    def parse(self):
        stmt_list = []
        while not self.isAtEnd():
            stmt_list.append(self.statement())
        return stmt_list

    def declaration_stmt(self, line):
        """
        Function to parse a DECLARE statement, e.g. DECLARE Num : INTEGER
        """

        # Now match an idenifier and get it's name
        if not self.match([TT.IDENTIFIER]):
            raise SyntaxError([self.previous().line, f"Declaration missing an identifier, got '{self.peek().lexeme}' instead"])

        name = self.previous().literal
        
        # Now match a colon
        if not self.match([TT.COLON]):
            raise SyntaxError([self.previous().line, f"Declaration missing ':', got '{self.peek().lexeme}' instead"])                   

        # Now match a valid data type
        if self.match([TT.ARRAY]):

            if not self.match([TT.LEFT_BRACK]):
                raise SyntaxError([self.previous().line, f"ARRAY declaration missing '[', got '{self.peek().lexeme}' instead"])
                        
            start = self.expression("ARRAY Start", line)

            if type(start.expression) != int:
                raise SyntaxError([self.previous().line, f"ARRAY declaration start index needs to be an integer'"])

            if not self.match([TT.COLON]):
                raise SyntaxError([self.previous().line, f"ARRAY declaration missing ':', got '{self.peek().lexeme}', expected INTEGER, REAL, STRING, BOOLEAN, CHAR"])
                            
            end = self.expression("ARRAY End", line)

            if type(end.expression) != int:
                raise SyntaxError([self.previous().line, f"ARRAY declaration end index needs to be an integer'"])

            if not self.match([TT.RIGHT_BRACK]):
                raise SyntaxError([self.previous().line, f"ARRAY declaration missing ']', got '{self.peek().lexeme}' instead"])
                                
            if not self.match([TT.OF]):
                raise SyntaxError([self.previous().line, f"ARRAY declaration missing 'OF', got '{self.peek().lexeme}' instead"])
                                                                    
            if not self.match([TT.INTEGER, TT.REAL, TT.STRING, TT.BOOLEAN, TT.CHAR]):
                raise SyntaxError([self.previous().line, f"ARRAY declaration missing valid type, got '{self.peek().lexeme}', expected INTEGER, REAL, STRING, BOOLEAN, CHAR"])
            
            return DECLARE_ARRAY(name, start, end, self.previous(), line)


        elif self.match([TT.INTEGER, TT.REAL, TT.STRING, TT.BOOLEAN, TT.CHAR]) :
            return DECLARE(name, self.previous(), line)

        else: # Invalid data type found
            raise SyntaxError([self.previous().line, f"Declaration missing valid type, found, got '{self.peek().lexeme}', expected INTEGER, REAL, STRING, BOOLEAN, CHAR"])
            

    def function_decl_stmt(self, line):
        """
        Parse a FUNCTION declaration, 

        e.g. FUNCTION IDENTIFIER RETURNS <type> ENDFUNCTION

        or FUNCTION IDENTIFIER (A: <type>, B<type>, ... ) RETURNS <type> ENDFUNCTION <- Not implemented yet
        """

        # Now match an idenifier and get it's name
        if not self.match([TT.IDENTIFIER]):
            raise SyntaxError([self.previous().line, f"Declaration missing an identifier, got '{self.peek().lexeme}' instead"])

        name = self.previous().literal

        args = self.param_list(line)

        # Now match RETURNS keyword
        if not self.match([TT.RETURNS]):
                raise SyntaxError([self.previous().line, f"Declaration missing 'RETURNS', got '{self.peek().lexeme}' instead"])                   

        # Now match a valid data type
        if not self.match([TT.INTEGER, TT.REAL, TT.STRING, TT.BOOLEAN, TT.CHAR, TT.ARRAY]):
            raise SyntaxError([self.previous().line, f"Declaration missing valid type, found, got '{self.peek().lexeme}', expected INTEGER, REAL, STRING, BOOLEAN, CHAR, ARRAY"])

        rtype = self.previous().type

        # Now get the function statement block - checks are made inside stmt_block for an empty stmt block or terminator not found 
        stmt_list = self.stmt_block([TT.ENDFUNCTION], line)

        return DECLARE_FUNCTION (name, args, stmt_list, rtype, line)

    def array_assign_stmt(self, name, line):
        
        # Found potential array identifier
        index = self.expression("Array index", line)

        if self.match([TT.RIGHT_BRACK]):
            if self.match([TT.ASSIGN]):
                expr = self.expression("Array assignment", line)
                return ARRAY_ASSIGN(name, index, expr, line)

            else:
                SyntaxError([line, f"Missing '<-' while parsing for array assignment"])

        else:
            raise SyntaxError([line, f"Unable to match ']' for array assignment"])

    def assign_stmt(self, name, line):
        """
        Function to parse an assignment statement, e.g. Num <- 42
        """

        # Now parse the expression
        expr = self.expression("Assignment statement", self.previous().line)

        if expr != None:
            return ASSIGN(name, expr, line)

        else: # Missing an expression
            raise SyntaxError([self.peek().line, f"Assignment missing an expression"] )


    def print_stmt(self, line):
        """
        Function to parse a PRINT statement, e.g. PRINT 4 + 3
        supports an expression list, i.e. PRINT 1, 2, 3
        """
        expr_list = []
        expr = self.expression("Print statement", self.previous().line)
        if expr == None: # Missing expression for PRINT
            raise SyntaxError([self.previous().line, f"Missing expression for PRINT or OUTPUT"] )

        expr_list.append(expr)
        while self.peek().type == TT.COMMA:
            self.advance()
            expr = self.expression("Print statement", self.previous().line)
            if expr == None: # Missing expression for PRINT
                raise SyntaxError([self.previous().line, f"Missing expression for PRINT or OUTPUT"] )

            expr_list.append(expr)
        
        return PRINT (expr_list, line) 

    def input_stmt(self, line):
        """
        Function to parse an INPUT statement, e.g. INPUT <identifier>
        identifier needs to be pre-declared.
        """

        if self.match([TT.IDENTIFIER]):
            name = self.previous().literal
            return INPUT (name, line)
        else:
            raise SyntaxError([self.previous().line, f"Missing identifier for INPUT"] )


    def stmt_block(self, block_terminator, line):
        """
        Function to parse a statement group

        :param block_terminator: Indicates the tokens to end a statement group
        :type: TokenType

        :return: List
        """
        
        # A list is used to store statements
        stmt_list = []

        # While we are not at the end of the program and we have found the terminator token
        while not self.isAtEnd() and not self.match(block_terminator):

            # call and add statement() to our statement list
            stmt_list.append(self.statement())

        # Syntax error, we reached the end of the program without finding a termninator
        if self.previous().type not in block_terminator:
            raise SyntaxError([line, f"Unexpected EOF while looking for '{block_terminator}'"] )

        # Syntax error, we didn't find any statements
        if len(stmt_list) == 0:
            raise SyntaxError([line, "Empty statement block"])

        return stmt_list

    def if_stmt(self, line):
        expr = self.expression("IF statement", self.previous().line)

        if not self.match([TT.THEN]):
            raise SyntaxError([self.peek().line, f"Expected 'THEN' got '{self.peek().lexeme}'"])

        else:
            stmt_list = self.stmt_block([TT.ENDIF, TT.ELSE], line)
            if self.previous().type == TT.ELSE:
                else_stmt_list = self.stmt_block([TT.ENDIF], line)
                return IF_ELSE (expr, stmt_list, else_stmt_list, line)
            else:
                return IF (expr, stmt_list, line)

    def while_stmt(self, line):

        # Get the condition        
        expr = self.expression("WHILE statement", self.previous().line)

        # Now match DO
        if not self.match([TT.DO]):
            raise SyntaxError([self.peek().line, f"Syntax: expected 'DO' got '{self.peek().lexeme}'"])

        else:            
            stmt_list = self.stmt_block([TT.ENDWHILE], line)
            return WHILE (expr, stmt_list, line)


    def repeat_stmt(self, line):

        # Get statement block
        stmt_list = self.stmt_block([TT.UNTIL], line)

        # Get the condition        
        expr = self.expression("REPEAT statement", self.previous().line)

        return REPEAT (expr, stmt_list, line)

    # Function to parse the parameter list for a function or a procedure
    def param_list(self, line):

        args = []

        if not self.match([TT.LEFT_PAREN]): # Function or procedure does not have parameters
            return args

        while not self.isAtEnd():
            if self.match([TT.RIGHT_PAREN]): # End of the param list
                return args

            if not self.match([TT.IDENTIFIER]):
                raise SyntaxError(line, f"Expected a parameter identifier, got a {self.peek().type}")

            name = self.previous().literal

            if not self.match([TT.COLON]):
                raise SyntaxError(line, f"Expected a type seperator :, got a {self.peek().type}")

            if not self.match([TT.INTEGER, TT.REAL, TT.STRING, TT.BOOLEAN, TT.CHAR, TT.ARRAY]):
                raise SyntaxError([self.previous().line, f"Declaration missing valid type, found, got '{self.peek().lexeme}', expected INTEGER, REAL, STRING, BOOLEAN, CHAR, ARRAY"])

            ptype = self.previous().type

            args.append((name, ptype))

            # try and match a comma
            self.match([TT.COMMA])
        
        raise SyntaxError(line, f"Unexpected EOF while parsing parameter list")


    def proc_stmt(self, name, line):

        args = []

        while not self.isAtEnd():
            args.append(self.expression("PROC_Statement", line))
            if self.match([TT.RIGHT_PAREN]):
                break

            elif self.match([TT.COMMA]):
                continue

        return CALL (name, args, line)


    def for_stmt(self, line):

        assign = None
        
        # now match an identifier
        if self.match([TT.IDENTIFIER]):

            name = self.previous().literal
            if self.match([TT.ASSIGN]):
                assign = self.assign_stmt(name, line) # e.g. I <- 1
            else:
                raise SyntaxError([line, f"FOR Missing '<-'"])

        if not isinstance(assign, ASSIGN):
            raise SyntaxError([line, f"Missing 'identifier <- expression'"])

        else:

            if not self.match([TT.TO]):
                raise SyntaxError([line, f"Expected TO, got '{self.peek().lexeme}'"])

            else:
                end = self.expression("FOR statement", self.previous().line)

                # Check if we have a 'STEP' keyword - this is optional
                step = None
                if self.match([TT.STEP]):
                    step = self.expression("FOR statement STEP", self.previous().line)

                # Get statement block
                stmt_list = self.stmt_block([TT.NEXT], line)

                if not self.match([TT.NEXT]) and not self.match([TT.IDENTIFIER]):
                    raise SyntaxError([self.previous().line, f"Expected NEXT followed by an Identifier"])

                else:
                    return FOR (assign, end, step, stmt_list, line)

    def return_stmt(self, line):
        return RETURN (self.expression("RETURN statement", line))

    def file_handling_stmt(self, line):

        if self.previous().type == TT.OPENFILE:
            expr = self.expression("OPENFILE statement", line)

            if not self.match([TT.FOR]):
                raise SyntaxError([line, f"Missing FOR for OPENFILE"])                 
            if not self.match([TT.READ, TT.WRITE, TT.APPEND]):
                raise SyntaxError([line, f"Invalid file mode {self.peek().literal}"])

            return OPENFILE (expr, self.previous().type, line)

        elif self.previous().type == TT.CLOSEFILE:
            expr = self.expression("CLOSEFILE statement", line)

            return CLOSEFILE (expr, line)

        elif self.previous().type == TT.READFILE:
            file_id = self.expression("READFILE statement", line)

            if not self.match([TT.COMMA]):
                raise SyntaxError([line, f"READFILE: expected a comma after the file id - got {self.peek().literal}"])

            if not self.match([TT.IDENTIFIER]):
                raise SyntaxError([line, f"READFILE: expected an identfier after the comma - got {self.peek().literal}"])

            return READFILE (file_id, self.previous().literal, line)

        elif self.previous().type == TT.WRITEFILE:
            file_id = self.expression("WRITEFILE statement", line)
         
            if not self.match([TT.COMMA]):
                raise SyntaxError([line, f"Expected a comma after the file id - got {self.peek().literal}"])

            expr = self.expression("WRITEFILE statement", line)

            return WRITEFILE (file_id, expr, line)

        raise SyntaxError([line, f"Expected file operation {self.previous().literal}"])

    def statement(self):

        if self.match([TT.DECLARE]):
            return self.declaration_stmt(self.previous().line)

        elif self.match([TT.IDENTIFIER]):

            name = self.previous().literal
            if self.match([TT.ASSIGN]):
                return self.assign_stmt(name, self.previous().line)

            elif self.match([TT.LEFT_PAREN]):
                return self.proc_stmt(name, self.previous().line)

            elif self.match([TT.LEFT_BRACK]):
                return self.array_assign_stmt(name, self.previous().line)

            else:
                raise SyntaxError([self.peek().line, f"Unexpected {self.peek().type.name} ('{self.peek().lexeme}') following IDENTIFIER ('{self.previous().lexeme}')"])

        elif self.match([TT.PRINT, TT.OUTPUT]):
            return self.print_stmt(self.previous().line)

        elif self.match([TT.INPUT]):
            return self.input_stmt(self.previous().line)

        elif self.match([TT.IF]):
            return self.if_stmt(self.previous().line)

        elif self.match([TT.WHILE]):
            return self.while_stmt(self.previous().line)

        elif self.match([TT.REPEAT]):
            return self.repeat_stmt(self.previous().line)

        elif self.match([TT.FOR]):
            return self.for_stmt(self.previous().line)

        elif self.match([TT.FUNCTION]):
            return self.function_decl_stmt(self.previous().line)

        elif self.match([TT.RETURN]):
            return self.return_stmt(self.previous().line)

        elif self.match([TT.OPENFILE, TT.CLOSEFILE, TT.READFILE, TT.WRITEFILE]):
            return self.file_handling_stmt(self.previous().line)

        else:
            self.advance()
            raise SyntaxError([self.previous().line, f"Unexpected token '{self.previous().lexeme}'"])

    def expression(self, stmt, line):
        expr = self.bool_or()

        if expr != None:
            return expr

        else: # Raise an exception if expression is empty
            raise SyntaxError([line, f"{stmt} missing an expression"])

    def bool_or(self):
        expr = self.bool_and()
        while self.match ( [TT.OR] ):
            operator = self.previous()
            right = self.comparision()
            expr = BINARY(expr, operator, right, operator.line)

        return expr

    def bool_and(self):
        expr = self.bool_not()
        while self.match ( [TT.AND] ):
            operator = self.previous()
            right = self.comparision()
            expr = BINARY(expr, operator, right, operator.line)
            
        return expr

    def bool_not(self):
        expr = self.comparision()
        while self.match ( [TT.NOT] ):
            operator = self.previous()
            right = self.comparision()
            expr = UNARY(operator, right)

        return expr

    def comparision(self):
        expr = self.term()

        while self.match([TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL, TT.LESS_GREATER, TT.BANG_EQUAL, TT.EQUAL, TT.BANG_EQUAL, TT.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = BINARY(expr, operator, right, operator.line)
            
        return expr

    def term(self):

        expr = self.factor()

        while self.match([TT.MINUS, TT.PLUS, TT.AMPERSAND ]):

            operator = self.previous()
            right = self.factor()

            expr = BINARY (expr, operator, right, operator.line)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match([TT.SLASH, TT.STAR, TT.DIV, TT.MOD] ):
            operator = self.previous()
            right = self.unary()
            expr = BINARY (expr, operator, right, operator.line)

        return expr

    def unary(self):
        if self.match([TT.BANG, TT.MINUS]):
            operator = self.previous()
            right = self.unary()
            return UNARY (operator, right)

        return self.primary()

    def primary(self):
        
        if self.match([TT.FALSE]): 
            return LITERAL (False)

        elif self.match([TT.TRUE]): 
            return LITERAL(True)

        elif self.match([TT.INTEGER, TT.REAL, TT.STRING, TT.QUOTE]):
            return LITERAL(self.previous().literal)

        elif self.match([TT.IDENTIFIER]):

            name = self.previous().lexeme
            line = self.previous().line

            # check if this is a variable or a function identifer
            if self.match([TT.LEFT_PAREN]): # found a function
                args = []
                while not self.match([TT.RIGHT_PAREN]):
                    args.append(self.expression("FUNCTION", self.peek().line))
                    self.match([TT.COMMA]) # consume a comma, if there is one
                    
                return FUNCTION (name, args, line)

            elif self.match([TT.LEFT_BRACK]): # check if it's an array identifier
                index = self.expression("ARRAY", line)
                
                if self.match([TT.RIGHT_BRACK]):
                    return ARRAY(name, index, line)
                else:
                    raise SyntaxError(line, f"array {name} missing ']'")
            else:
                return IDENTIFIER(name)

        elif self.match([TT.LEFT_PAREN]):
            expr = self.expression("( ... )", self.previous().line)

            if self.match([TT.RIGHT_PAREN]):
                return GROUPING(expr)

            else:
                raise SyntaxError([self.peek().line, "Missing closing ')'"])

        return None

    def match(self, tokens):

        if self.peek().type in tokens:
            self.advance()
            return True

        return False



