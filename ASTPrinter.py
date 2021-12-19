import Parser

class ASTPrinter:
    def __init__(self, tree):
        self.tree = tree

    def print(self):
        self.visitNode(self.tree) 
        print()

    def visitNode(self, expr):

        if isinstance(expr, Parser.LITERAL_Expr): # Reached the leaves
            print(f"{expr.expression}", end=" ")

        elif isinstance(expr, Parser.BINARY_Expr): # Post-order tree traversal 
            self.visitNode(expr.left)
            self.visitNode(expr.right)
            print(f"{expr.operator.lexeme}", end=" ")

        elif isinstance(expr, Parser.GROUPING_Expr):
            self.visitNode(expr.expression)

        elif isinstance(expr, Parser.UNARY_Expr):
            self.visitNode(expr.right)
            print(f"{expr.operator.lexeme}", end=" ")