import logging
logger = logging.getLogger(__name__)

# sample parsed data
# {'commandType': 'C_PUSH', 'arg1': 'constant', 'arg2': '82'}

# Counters for Stack

SP = 0

def getSP(SP):
    
    if SP == 0:        
        return 256
    elif SP > 0:
        return 256 + SP

def code(parsed):       
    
    logger.info(len(parsed))
    
    output = []
    
    for line in parsed:
        logger.debug('Command type is %s' % line['commandType'])
        result = writeLine(line)       
        output.extend(result)
    
    return output    
    
        
def writeLine(line):
    
    commandType = line['commandType']
    
    if commandType == 'C_ARITHMETIC':
        result = writeArithmetic(line)
    elif commandType == ('C_PUSH' or 'C_POP'):
        result = writePushPop(line)
        
    return result
    
def writeArithmetic(line):
    
    # {'commandType': 'C_ARITHMETIC', 'arg1': 'sub', 'arg2': None}
    
    if line['arg1'] == 'add':
        result = add() # ["I'm an arithmetic line!"]
    
        return result
    
    return ["I'm an arithmetic line!"]

def writePushPop(line):
    
    # The stack: mapped on RAM[256 ... 2047];
    # The stack pointer is kept in RAM address SP    
    
    commandType = line['commandType']

    if commandType == 'C_PUSH':
        result = writePush(line)
    elif commandType == 'C_POP':
        result = writePop(line)
    
    return result

def aCommand(arg):

    aCommands =    {'add'           :      '+'  , # Binary
                    'sub'           :      '-'  , # Binary
                    'neg'           :      '-'  , # Unary
                    'eq'            :       eqCommand()  , # Unary using JMP
                    'gt'            :       gtCommand()  , # Unary using JMP
                    'lt'            :       ltCommand()  , # Unary using JMP
                    'and'           :       '&'  , # Binary
                    'or'            :       orCommand()  , # Binary
                    'not'           :       '!' # Unary
    
                   }

def addCommand():
    # add first 2 items in stack [256, 257]
    
    result = []
    
    commands = [ '@SP', # Stack Pointer
                 'A=M', # Go to memory address in pointer eg. 256
                 'A=A-1', # We're not writing anything new to the stack so go back one item to last written
                 'D=M', # Set D register to contents of top most stack item               
                 'M=0', # Clear that register                 
                 'A=A-1', # Go to the new top of stack               
                 'M=D+M', # Calculate the sum of the value in D and the current register and replace its contents with it
                 '@SP',
                 'M=M-1' # Decrement the stack pointer
                ]    
          
    result.extend(commands)
    return result



def writePush(line):
    
    # {'commandType': 'C_PUSH', 'arg1': 'constant', 'arg2': '82'}    
    
    # @address
    # M=arg2
    
    result = []
    
    if line['arg1'] == 'constant':
    
        commands = [ '@%s' % line['arg2'],
                     'D=A',
                     '@SP',                     
                     'A=M',
                     'M=D',
                     '@SP',
                     #'@increment',
                     #'M;JGT',
                     #'(increment)',
                     'M=M+1'
                    ]
        
        # result.append('@%s' % line['arg2']) #getSP()+1)
        # result.append('D=A')
        # 
        # result.append('@SP')
        # result.append('M=D')
        result.extend(commands)
    
    
    logger.debug('Commands: %s' % commands)
    return result # "I'm a push paddle line!"

def writePop(line):
    
    # {'commandType': 'C_POP', 'arg1': 'constant', 'arg2': '82'}    
    
    return ["I'm a paddle pop line!"]

