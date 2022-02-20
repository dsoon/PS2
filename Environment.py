class Environment:

    global_variables = {}
    scopes = [] # stack of Environments

    def __init__(self):
        self.variables = {}

    def push(env):
        Environment.scopes.insert(0, env)

    def pop():
        Environment.scopes.pop(0)

    def add_variable(symbol):

        # Get current scope
        scope = Environment.global_variables
        if len(Environment.scopes) != 0:
            scope = Environment.scopes[0].variables
            
        if symbol.vname not in scope:
            scope[symbol.vname] = symbol
        else:
            pass # symbol was previously defined ... skip

    def get_variable(vname):

        symbol = None

        if len(Environment.scopes) != 0:
            for i in range(len(Environment.scopes)):
                scope = Environment.scopes[i].variables
                
                if vname in scope:
                    symbol = scope[vname]
                    break

            if symbol == None and vname in Environment.global_variables: # check to see if it's a global
                symbol = Environment.global_variables[vname]

        else:
            if vname in Environment.global_variables:
                symbol = Environment.global_variables[vname]

        if symbol == None:
            raise NameError(f"Variable '{vname}' not declared")
        else:
            return symbol

    def remove_variable(vname):

        found = False

        if len(Environment.scopes) != 0:
            for i in range(len(Environment.scopes)):
                scope = Environment.scopes[i].variables
                
                if vname in scope:
                    del scope[vname]
                    found = True
                    break

            if not found and vname in Environment.global_variables: # check to see if it's a global
                del Environment.global_variables[vname]

        else:
            if vname in Environment.global_variables:
                del Environment.global_variables[vname]
                found = True

        if not found:
            raise NameError(f"Variable '{vname}' not declared")

    def symbol_defined(vname):

       # Get current scope
        scope = Environment.global_variables
        if len(Environment.scopes) != 0:
            scope = Environment.scopes[0].variables

        return vname in scope

    def reset():

        # Get current scope
        scope = Environment.global_variables
        if len(Environment.scopes) != 0:
            scope = Environment.scopes[0].variables

        scope = {}

    def dump_variables():

       # Get current scope
        scope = Environment.global_variables
        if len(Environment.scopes) != 0:
            scope = Environment.scopes[0].variables

        keys=scope.keys()
        print("Variables:")
        if keys != None:
            for k in keys:
                print(f"{scope[k]}")

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

class File_Symbol(Symbol):
    def __init__(self, name, mode, _fileid):
        Symbol.__init__(self, name, None)
        self.mode = mode
        self._fileid = _fileid
        self.isEOF = False

class Function_Symbol(Symbol):
    def __init__(self, name, args, rtype, stmt_list, line):
        Symbol.__init__(self, name, rtype)
        self.args = args
        self.rtype = rtype
        self.stmt_list = stmt_list
        self.line = line

    def __str__(self):
        return f"Function symbol name={self.vname} | returns={self.vtype} | args={self.args} | statement_list={self.stmt_list}"

#class Return_Symbol(Symbol):
#    def __init__(self, value):
#        self.vname = "__return__"
#        self.value = value
