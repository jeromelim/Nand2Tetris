'''
Parser for Hack Assembly Language

Encapsulates access to the input code. Reads an assembly language command,
parses it, and provides convenient access to the command?s components
(fields and symbols). In addition, removes all white space and comments.

'''
import settings
import os
import code
import symboltable

print "parser loaded"


def loadFile(filepath):
    
    lines = []
    
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n\r') for line in f if line != '\n']

        return lines
    
def saveFile(datafile, filepath):
    
    # change output file to .hack
    
    filename = filepath.split('\\')[-1]
    filename = filename.replace('asm','hack')
    filepath = os.path.join(settings.savepath,filename)
    print filename
    print filepath
    print 'datafile', datafile
    with open(filepath, 'w') as f:
        for line in datafile[:-1]:
            f.write(line)
            f.write('\n')        
        f.write(datafile[-1])
          
def remove_comments(line):
    code = line.split('//')[0]
    if code:
        return line.split('//')[0].strip()
    return False

def commandType(line):
    
    # Returns type of command
    
    if '@' in line:
        #print 'A_COMMAND'
        return 'A_COMMAND'
    if (line.startswith('(') and line.endswith(')')):
        return 'L_COMMAND'
    if '=' in line or ';' in line:
        #print C_COMMAND(line)
        return 'C_COMMAND'
    
def parsecommand(line, commandtype):
    
    if commandtype == 'A_COMMAND':
        return A_COMMAND(line)
    if commandtype == 'C_COMMAND':
        return C_COMMAND(line)
    if commandtype == 'L_COMMAND':
        return L_COMMAND(line)

def A_COMMAND(line):
    return line.split('@')[-1]

def L_COMMAND(line):
    return line.strip('(').strip(')')

def C_COMMAND(line):
    
    if ';' in line:
        jump = line.split(';')[-1].strip()
    else:
        jump = 'null'
    
    if '=' in line:
        dest = line.split('=')[0].strip()
    else:
        dest = 'null'
    
    comp = line.split('=')[-1].split(';')[0].strip()
    
    return dest, comp, jump

def handlesymbols(line):
          
    line = code.toBinary(symboltable.convert(line))           
            
    return line

def parse(filepath):

    datafile = loadFile(filepath)
    
    output1 = []
    output = []
    symbols = symboltable.SymbolTable()  
    
    # First pass to remove comments and whitespace, add 
    
    for line in datafile:
        line = remove_comments(line)
        if line:
            
            print 'command type is %s' % commandType(line)
            if commandType(line) == 'L_COMMAND':
                symbols[L_COMMAND(line)] = len(output1)
                    
            else:
                output1.append(line)
        
    print 'output1', output1             
    
                
    for id, line in enumerate(output1):
        
        command = commandType(line)
        commands = parsecommand(line, command)
        print 'command', command
        print 'commands', commands
        print 'id', id
        #print 'symbols', symbols.table
        print 'line', line
        
        if command == 'A_COMMAND':
            
            if commands.isdigit():
                output.append(code.toBinary(int(commands)))
            
            elif commands in symbols:
                commands = int(symbols[commands])
                print 'commands in symbols'
                output.append(code.toBinary(commands))#code.toBinary(int(line.replace(commands.split('@')[-1], str(symbols[commands.split('@')[-1]]))))
                #print 'output[id]', output[id]
                
            elif commands not in symbols:
                symbols.addVariable(commands)
                address = symbols[commands]
                output.append(code.toBinary(address))
            '''
            else:
               encoded = code.code(command, commands)
               print 'encoded = %s' % encoded
               output.append(encoded) # code.toBinary(int(encoded))
               print 'output[id]', output[id]
            '''
        else:                                 
        
            command = commandType(line)
            commands = parsecommand(line, command)
            if command == 'C_COMMAND':
                encoded = code.code(command, commands)
                if encoded:
                    output.append(encoded)
                    
                else:
                   pass#output[id] = line
                print len(output), commands, line, encoded
            
    #output = handlesymbols(output)            

    # Remove last line feed            
    #output[-1] = output[-1].replace('\n','')
            
    saveFile(output, filepath)