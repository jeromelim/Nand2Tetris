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

def code(parsed, filename):       
    
    logger.info(len(parsed))
    
    output = []
    
    for line in parsed:
        logger.debug(('Command type is %s' % line['commandType']))
        result = writeLine(line, filename)       
        output.extend(result)
        
    
    return output    
    
        
def writeLine(line, filename):
    
    commandType = line['commandType']
    
    if commandType == 'C_ARITHMETIC':
        result = writeArithmetic(line)
    elif commandType == 'C_PUSH' or commandType == 'C_POP':
        result = writePushPop(line, filename)
        
        
    return result
    
def writeArithmetic(line):
    
    # {'commandType': 'C_ARITHMETIC', 'arg1': 'sub', 'arg2': None}
    result = commandChooser(line['arg1'])
    logger.debug(line['arg1'])
        
    logger.debug('writeArithmetic: %s' % result)
    
    return result

def writePushPop(line, filename):
    
    # The stack: mapped on RAM[256 ... 2047];
    # The stack pointer is kept in RAM address SP    
    
    commandType = line['commandType']

    if commandType == 'C_PUSH':
        result = writePush(line, filename)
    elif commandType == 'C_POP':
        result = writePop(line, filename)
    
    logger.debug('writePushPop: %s' % result)    
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


# Returns the memory segment specific assembly code

memCommands = {

                'static'   : [
                                '@FILENAME.arg2', # LCL is a pointer that holds the base address of the local segment
                                'A=arg2', # Go to address - arg2 in this case is the offset from the base address
                                
                                'D=M', # Store the value of the register at local base + offset in D register                                
                             ], 

                'constant' : [
                                '@arg2', # Constant is similar to @arg2,
                              
                                'D=A' # Store address value in D register                                
                             ],
                
                'local'    : [
                                '@LCL', # LCL is a pointer that holds the base address of the local segment
                                'D=M', # Store base address in D register
                                '@arg2', # Go to address - arg2 in this case is the offset from the base address
                                'D=D+A', # Add offset to base address
                                'A=D', # Go to selected address
                                
                                'D=M', # Store the value of the register in D register                                
                             ],
                    
                'argument' : [
                                '@ARG', # LCL is a pointer that holds the base address of the local segment
                                'A=arg2', # Go to address - arg2 in this case is the offset from the base address
                                
                                'D=M', # Store the value of the register at local base + offset in D register                                
                             ],                    
                
                }

def updateVariables(lines, command, arg2, filename):
    
    for id, line in enumerate(lines):
        replaced = line.replace('FILENAME', filename)
        replaced = line.replace('arg2', arg2)
        lines[id] = replaced
    
    return lines

def writePush(line, filename):
    
    # Gets value from specified memory segment[arg2] and adds it to top of stack
    # Increments Stack Pointer
    
    # {'commandType': 'C_PUSH', 'arg1': 'constant', 'arg2': '82'}    
    
    # @address
    # M=arg2
    command, arg2 = line['arg1'], line['arg2']
    
    result = []
    
    getValue = memCommands[command]
    updatedVariables = updateVariables(getValue, command, arg2, filename)
    
    pushMain = [
                 '@SP', # Go to stack pointer                    
                 'A=M', # Go to address referenced by stack pointer
                 
                 'M=D', # Set contents of memory address to D (arg2)
                 
                 '@SP', # Increment stack pointer
                 'M=M+1'
               ]

    result.extend(updatedVariables)
    result.extend(pushMain)
            
    logger.debug('Commands: %s' % result)
    
    return result 

def writePop(line, filename):
    
    # Gets value from top of stack and assigns it to specified memory segment[arg2]
    # 
    
    # {'commandType': 'C_POP', 'arg1': 'constant', 'arg2': '82'}
    
    popMain = [ 
                                  
                 '@SP', # Go to stack pointer                    
                 'A=M', # Go to address referenced by stack pointer
                 'A=A-1', # Decrement address to get last item in stack
                 
                 'D=M', # Store contents of stack in D Register
                                                   
                 '@SP', # Decrement stack pointer (No need to clear previous register - it will just be overwritten with new data)
                 'M=M-1',
                 
                 # Go to specified memory segment[index]
                 # Set contents as D Register
                 
                ]    
    
    return popMain

