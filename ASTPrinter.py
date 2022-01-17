import Parser

class ASTPrinter:
    '''
    Abstract Syntax Tree Printer
    ============================
    '''
    def __init__(self, tree):
        self.tree = tree

    def print(self):
        self.visit(self.tree) 
        print()

    def visit(self, expr):
        """
        Visit an expression node.
            if expression is a LITERAL_Expr then print its value

            if expression is a BINARY_Expr, visit its left nodem right node then print its value

            if expression is a GROUPING_Expr, visit its expression

            if expression is a UNARY_Expr, visit its right node and print its value

        :param expr: an expression node
        :type expr: Expr

        :return None: method does not return a value
        :type None: N/A
        """

        if isinstance(expr, Parser.LITERAL_Expr): # Reached the leaves
            print(f"{expr.expression}", end=" ")

        elif isinstance(expr, Parser.BINARY_Expr): # Post-order tree traversal 
            self.visit(expr.left)
            self.visit(expr.right)
            print(f"{expr.operator.lexeme}", end=" ")

        elif isinstance(expr, Parser.GROUPING_Expr):
            self.visit(expr.expression)

        elif isinstance(expr, Parser.UNARY_Expr):
            self.visit(expr.right)
            print(f"{expr.operator.lexeme}", end=" ")