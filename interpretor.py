
class Interpretor:

    def __init__(self, stmt_list):
        self.stmt_list = stmt_list

    def interpret(self):

        if self.stmt_list != None:

            for stmt in self.stmt_list:
                
                try:

                    stmt.interpret()

                except NameError as ne:
                    raise RuntimeError([stmt.line, f"{ne}"])
            