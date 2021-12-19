from Token import TokenType as TT
import Parser

class Interpretor:
    def __init__(self, tree):
        self.tree = tree

    def interpret(self):
        return self.visitNode(self.tree) 

    def visitNode(self, expr):

        if isinstance(expr, Parser.LITERAL_Expr): # Reached the leaves
            return expr.expression

        elif isinstance(expr, Parser.BINARY_Expr): # Post-order tree traversal 

            left  = self.visitNode(expr.left)
            right = self.visitNode(expr.right)

            op = expr.operator.type
            
            if  op == TT.PLUS:
                return left + right

            elif op  == TT.MINUS:
                return left - right

            elif op  == TT.STAR:
                return left * right

            elif op  == TT.SLASH:
                return left / right

            elif op  == TT.GREATER:
                return left > right

            else:
                print(f"Interpretor: Unecognised binary operator '{expr.operator.lexeme}' on line {expr.operator.line}")

        elif isinstance(expr, Parser.GROUPING_Expr):
            return self.visitNode(expr.expression)

        elif isinstance(expr, Parser.UNARY_Expr):
            right  = self.visitNode(expr.right)
            if expr.operator.lexeme == '-':
                return -right
            