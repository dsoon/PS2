class Environment:

    global_variables = {}

    def __init__(self):
        self.variables = {}

    def add_variable(self, vname, vtype):
        pass

    def add_variable(symbol):

        # Check that the variable hasn't already been declared 
        if symbol.vname in Environment.global_variables:
            raise NameError(f"Variable '{symbol.vname}' already declared")

        else:
            Environment.global_variables[symbol.vname] = symbol

    def get_variable(vname):

        # Check is the variable has been declared
        if vname not in Environment.global_variables:
            raise NameError(f"Variable '{vname}' not declared")
        else:
            return Environment.global_variables[vname] 

    def reset():
        Environment.global_variables = {}

    def dump_global_variables():

        keys=Environment.global_variables.keys()
        print("Global variables:")
        if keys != None:
            for k in keys:
                print(f"{Environment.global_variables[k]}")

class Symbol:
    def __init__(self, vname, vtype, value=None):
        self.vname  = vname
        self.vtype = vtype
        self.value = value

    def __str__(self):
        return f"Symbol name={self.vname} | type={self.vtype} | value={self.value}"

class Array_Symbol(Symbol):
    def __init__(self, vname, vtype, s_idx, e_idx):
        Symbol.__init__(self, vname, vtype, value=[None for _ in range(e_idx-s_idx+1)])
        self.s_idx = s_idx
        self.e_idx = e_idx

    def __str__(self):
        return f"Array symbol name={self.vname} | type={self.vtype} | start={self.s_idx} | end={self.e_idx} value={self.value}"
