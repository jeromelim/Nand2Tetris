import logging
import VMSettings

logger = logging.getLogger(__name__)

# sample parsed data
# {'commandType': 'C_PUSH', 'arg1': 'constant', 'arg2': '82'}

# Counters for Stack

def getSP(SP):
    
    if SP == 0:        
        return 256
    elif SP > 0:
        return 256 + SP
    
def counter(i):
    while True:
        i = i + 1
        yield i
        
jumpCounter = counter(0)

def code(parsed):       
    
    logger.info(len(parsed))
    
    output = []
    
    for line in parsed:
        logger.debug(('Command type is %s' % line['commandType']))
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
    result = commandChooser(line['arg1'])
    logger.debug(line['arg1'])
    
    logger.debug(result)
    
    return result

def writePushPop(line):
    
    # The stack: mapped on RAM[256 ... 2047];
    # The stack pointer is kept in RAM address SP    
    
    commandType = line['commandType']

    if commandType == 'C_PUSH':
        result = writePush(line)
    elif commandType == 'C_POP':
        result = writePop(line)
    
    return result

def commandChooser(command):
    # Chooses command based designated type
    commandType, operator = VMSettings.aCommands[command]
    logger.debug(('commandType, operator', commandType, operator ))
    if commandType == 0:
        result = unaryCommand(operator)
    elif commandType == 1:
        result = binaryCommand(operator)
    elif commandType == -1:
        result = jumpCommand(operator)
        
    return result
        
def unaryCommand(operator):
    # Apply chosen command to first item in stack, leaving the result the only item in stack
    logger.info('unary: %s' % operator)
    
    result = []
    
    commands = [ '@SP', # Stack Pointer
                 'A=M', # Go to memory address in pointer eg. 256
                 'A=A-1', # We're not writing anything new to the stack so go back one item to last written
                 'M=%sM' % operator, # Add unary operator
                ]    
          
    result.extend(commands)
    return result

def binaryCommand(operator):
    # Apply chosen command to first 2 items in stack, leaving the result the only item in stack
    logger.info('binary: %s' % operator)
    
    result = []
    
    commands = [ '@SP', # Stack Pointer
                 'A=M', # Go to memory address in pointer eg. 256
                 'A=A-1', # We're not writing anything new to the stack so go back one item to last written
                 'D=M', # Set D register to contents of top most stack item               
                 'M=0', # Clear that register                 
                 'A=A-1', # Go to the new top of stack               
                 'M=M%sD' % operator, # Calculate the sum of the value in D and the current register and replace its contents with it
                 '@SP',
                 'M=M-1' # Decrement the stack pointer
                ]    
          
    result.extend(commands)
    
    logger.debug(commands)
    
    return result

def jumpCommand(operator):

    # Apply chosen command to first 2 items in stack, leaving the result the only item in stack
    logger.info('jump: %s' % operator)
    jumpLabel = 'endJump%s' % next(jumpCounter)
    trueLabel = next(jumpCounter)
    
    result = []
    
    
    #subtract A-A=0
    subtractNumbers = binaryCommand('-')   
    
    commands = [ '@SP', # Stack Pointer
                 'A=M', # Go to memory address in pointer eg. 256
                 'A=A-1', # We're not writing anything new to the stack so go back one item to last written
                 'D=M', # Set D register to contents of top most stack item               
                 '@true%s' % trueLabel,
                 'D;%s' % operator, 
                 '@SP',
                 'A=M',
                 'A=A-1',#
                 'M=0',
                 '@%s' % jumpLabel,
                 '0;JMP',
                 '(true%s)' % trueLabel,
                 '@SP',
                 'A=M',
                 'A=A-1',
                 'M=-1',
                 '@SP',
                  #'M=M+1',
                 '(%s)' % jumpLabel
                ]
    #if 'J' in operator:
         
    result.extend(subtractNumbers)
   
    result.extend(commands)
    
    logger.debug(commands)
    
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
                     'M=M+1'
                    ]

        result.extend(commands)
    
    
    logger.debug('Commands: %s' % commands)
    return result # "I'm a push paddle line!"

def writePop(line):
    
    # {'commandType': 'C_POP', 'arg1': 'constant', 'arg2': '82'}    
    
    return ["I'm a paddle pop line!"]

