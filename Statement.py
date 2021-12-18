from abc import ABC

class Statement(ABC):
    pass

class IF_Statement(Statement):
    def __init__(self, condition, statement_list):
        self.condition = condition
        self.statement_list = statement_list

class CASE_Statement(Statement):
    def __init__(self):
        pass
