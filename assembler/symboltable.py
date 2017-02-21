print "symboltable loaded"

builtinSymbols = {  'SP'          :       0 ,
                    'LCL'         :       1 ,
                    'ARG'         :       2 ,
                    'THIS'        :       3 ,
                    'THAT'        :       4 ,
                    'R0'          :       0 ,
                    'R1'          :       1 ,
                    'R2'          :       2 ,
                    'R3'          :       3 ,
                    'R4'          :       4 ,
                    'R5'          :       5 ,
                    'R6'          :       6 ,
                    'R7'          :       7 ,
                    'R8'          :       8 ,
                    'R9'          :       9 ,
                    'R10'         :       10,
                    'R11'         :       11,
                    'R12'         :       12,
                    'R13'         :       13,
                    'R14'         :       14,
                    'R15'         :       15,
                    'SCREEN'      :       16384,
                    'KBD'         :       24576 }

class SymbolTable:

    table = builtinSymbols
    
    def __init__(self):
        self.variableNo = 16
        
    def __setitem__(self, symbol, address):
        self.table[symbol] = address
        
    def __getitem__(self, symbol):
        return self.table[symbol]
    
    def __contains__(self, symbol):
        return symbol in self.table
    
    def addVariable(self,symbol):
        self.table[symbol] = self.variableNo
        self.variableNo +=1
        


def main():
    return 'placeholder symboltable'

def convert(command, symbols={}):
    
    print 'symboltable.convert', command
    print 'is %s in symbols?' % command
    if command in builtinSymbols:
        print 'yes in symbols'
        print builtin(command)
        return builtin(command)
    else:
        # Check if variable is already added to symboltable
        
        if command in symbols:
            return symbols[command]
        
        # If not then add to symboltable    
        
        else:
                   
            pass

def builtin(symbol):
    try:
        return builtinSymbols[symbol]
    except:
        return symbol

print builtin('SCREEN')
    
print builtin('R2')    