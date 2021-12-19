from abc import ABC

from Token import TokenType as TT
import PS2

class Expr(ABC):
    def accept(self, visitor):
        pass

class UNARY_Expr(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class BINARY_Expr(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class LITERAL_Expr(Expr):
    def __init__(self, expression):
        self.expression = expression

class GROUPING_Expr(Expr):
    def __init__(self, expression):
        self.expression = expression

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        #print(f"peek current={self.current}")
        return self.tokens[self.current]

    def advance(self):
        if self.current < len(self.tokens):
            tok = self.tokens[self.current]
            self.current += 1
            return tok
        else:
            PS2.PS2.error(self.tokens[self.current].line, "unexpected EOF")

    def previous(self):
        if self.current > 0:
            return self.tokens[self.current - 1]
        else:
            PS2.PS2.error(self.tokens[self.current].line, "Call to Parser.previous without previous token")            

    def parse(self):
        return self.expression()

    def expression(self):
	    return self.equality()

    def equality(self):
	    expr = self.comparision()
	    while self.match ( [TT.BANG_EQUAL, TT.EQUAL_EQUAL] ):
		    operator = self.previous()
		    right = self.comparision()
		    expr = BINARY_Expr(expr, operator, right)

	    return expr

    def comparision(self):
        expr = self.term()

        while self.match([TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = BINARY_Expr(expr, operator, right)
        return expr

    def term(self):

        expr = self.factor()

        while self.match([TT.MINUS, TT.PLUS]):

            operator = self.previous()
            right = self.factor()

            expr = BINARY_Expr(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match([TT.SLASH, TT.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = BINARY_Expr(expr, operator, right)

        return expr

    def unary(self):
        if self.match([TT.BANG, TT.MINUS]):
            operator = self.previous()
            right = self.unary()
            return UNARY_Expr(operator, right)

        return self.primary()

    def primary(self):
        
        if self.match([TT.FALSE]): 
            return LITERAL_Expr(False)

        if self.match([TT.TRUE]): 
            return LITERAL_Expr(True)

        if self.match([TT.INTEGER, TT.REAL, TT.STRING]): 
            return LITERAL_Expr(self.previous().literal)

        if self.match([TT.LEFT_PAREN]):
            expr = self.expression()

            if self.match([TT.RIGHT_PAREN]):
                return GROUPING_Expr(expr)

            else:
                PS2.PS2.error(self.tokens[self.current].line, "missing ')'")


    def match(self, tokens):

        if self.peek().type in tokens:
            self.advance()
            return True

        return False



