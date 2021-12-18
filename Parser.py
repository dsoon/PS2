from abc import ABC

import Token
import PS2

class Expr(ABC):
    def accept(self, visitor):
        pass

class BINARY_Expr(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class LITERAL_Expr(Expr):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

'''
class Stmt(ABC):
    def accept(self, visitor):
        pass

class IF_Stmt(Stmt):
    def __init__(self, condition, statement_list):
        self.condition = condition
        self.statement_list = statement_list


class IF_ELSE_Stmt(Stmt):
    def __init__(self, condition, true_statement_list, false_statement_list):
        self.condition = condition
        self.true_statement_list = true_statement_list
        self.false_statement_list = false_statement_list

class CASE_Stmt(Stmt):
    def __init__(self, of, case_body_list, otherwise_statement_list):
        self.of = of
        self.case_body_list = case_body_list
        self.otherwise_statement_list
'''

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
            PS2.PS2.error(self.tokens[self.current].line, "unexpected EOF")

    def parse(self):
        return self.expression()

    def expression(self):
        if self.peek() == Token.TokenType.IDENTIFIER:
            id = self.advance()
            if self.peek() == Token.TokenType.OPERATOR:
                return Binary_Expr(id, self.advance(), self.expression()
        elif self.peek() == Token.TokenType.INTEGER:
            


        
        
        