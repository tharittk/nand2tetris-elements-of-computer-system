
# Symbol table

class SymbolTable():
    def __init__(self):
        self.table = {}

    # emties the symbol table, called when compiling new subroutine
    def reset(self):
        self.table = {}
    
    # add a new entry to the table: name (string), type (string), kind (STATIC, FIELD, ARG, or VAR), index
    def define(self, entryName, entryType, entryKind):
        self.table[entryName] = {}
        self.table[entryName]['type'] = entryType
        self.table[entryName]['kind'] = entryKind
        self.table[entryName]['index'] = self.varCount(entryKind) - 1
    
    # return the number of variable of a given kind
    def varCount(self, kind):
        count = 0
        for key in self.table.keys():
            if self.table[key]['kind'] == kind:
                count  += 1
        return count
    
    # return kind of the named identifier, if not found, return None
    def kindOf(self, name):
        if name in self.table.keys():
            return self.table[name]['kind']
        else:
            return None
    
    # return type of the named identifie
    def typeOf(self, name):
        if name in self.table.keys():
            return self.table[name]['type']
        
        else:
            return None

    # return type of the named identifie
    def indexOf(self, name):
        if name in self.table.keys():
            return self.table[name]['index']
        else:
            return None
