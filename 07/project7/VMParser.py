from VMUtils import *
import logging
logger = logging.getLogger(__name__)
import VMSettings

def process(file):
    
    logger.info('Load VM File into memory')
    
    fileContent = loadFile(file)
    
    # Parse it
          
    for line in fileContent:
        removed_comments = remove_comments(line)
        parsed = parse(removed_comments)
        if removed_comments != False:
            logger.debug(parsed)
        
        
    # Write machine code
    
    # Save to new file
    
    return True

def parse(line):
    parsed = {'commandType' : '', 'arg1' : '', 'arg2' : ''}
    parsed['commandType'] = commandType(line)
    parsed['arg1'] = arg1(line)
    parsed['arg2'] = arg2(line)
    logger.debug(parsed)
    #logger.debug('Command Type is %s arg1 is %s and arg2 is %s : %s' % (commandType(line), arg1(line), arg2(line), line))
    return parsed

def commandType(line):
    
    # Returns type of command
    
    for item in VMSettings.commandTypes:
        if item in str(line):
            return VMSettings.commandTypes[item]
        
def get_token(line, index):
    
    # Splits tokens and returns selected one
    
    tokens = str(line).split(' ')
    return tokens[index]    

def arg1(line):
    
    # Returns first argument of command
    
    try:
        arg1 = get_token(line, 1)
    except:
        arg1 = get_token(line, 0)
    return arg1

def arg2(line):
    
    # Returns first argument of command
    
    try:
        arg2 = get_token(line, 2)
        
        return arg2
    except:
        return None