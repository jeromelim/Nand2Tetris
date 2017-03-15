print "code loaded"
import symboltable

compTable = {   '0'   :    ('101010' , '0'),          
                '1'   :    ('111111' , '0'),          
                '-1'  :    ('111010' , '0'),          
                'D'   :    ('001100' , '0'),         
                'A'   :    ('110000' , '0'),         
                'M'   :    ('110000' , '1'),         
                '!D'  :    ('001101' , '0'),         
                '!A'  :    ('110001' , '0'),         
                '!M'  :    ('110001' , '1'),        
                '-D'  :    ('001111' , '0'),         
                '-A'  :    ('110011' , '0'),         
                '-M'  :    ('110011' , '1'),         
                'D+1' :    ('011111' , '0'),         
                'A+1' :    ('110111' , '0'),         
                'M+1' :    ('110111' , '1'),         
                'D-1' :    ('001110' , '0'),         
                'A-1' :    ('110010' , '0'),         
                'M-1' :    ('110010' , '1'),         
                'D+A' :    ('000010' , '0'),         
                'D+M' :    ('000010' , '1'),         
                'D-A' :    ('010011' , '0'),         
                'D-M' :    ('010011' , '1'),         
                'A-D' :    ('000111' , '0'),         
                'M-D' :    ('000111' , '1'),         
                'D&A' :    ('000000' , '0'),         
                'D&M' :    ('000000' , '1'),         
                'D|A' :    ('010101' , '0'),         
                'D|M' :    ('010101' , '1')   }

destTable = {   'null'   :   '000',
                'M'      :   '001',     
                'D'      :   '010',     
                'MD'     :   '011',    
                'A'      :   '100',     
                'AM'     :   '101',    
                'AD'     :   '110',    
                'AMD'    :   '111'   }

jumpTable = {   'null'    :   '000',
                'JGT'     :   '001',
                'JEQ'     :   '010',
                'JGE'     :   '011',
                'JLT'     :   '100',
                'JNE'     :   '101',
                'JLE'     :   '110',
                'JMP'     :   '111'   }

def toBinary(number):
    
    # Divide by 2 till the quotient is 0
    
    stack = []
    
    quotient = number
    
    while quotient > 0:
        quotient, remainder = divmod(quotient, 2)
        stack.append(str(remainder))
    
    stack.reverse()
    binary = ''.join(stack).zfill(16)
    
    return binary

    

def code(command, commands):
    
    print command, commands
    if command == 'C_COMMAND':
        
        binary = '111' + comp(commands[1]) + dest(commands[0]) + jump(commands[2])
        
        return binary
    
    elif command == 'A_COMMAND':
        
        if commands.isdigit():
        
            binary = toBinary(int(commands))
            
        else:
            
            converted = symboltable.convert(commands)
            print commands
            binary = toBinary(int(converted))
            #binary = toBinary(int(commands)) # toBinary(int(converted))
        
        return binary
    
def dest(mnemonic):
    binary = destTable[mnemonic]
    return binary

def jump(mnemonic):
    binary = jumpTable[mnemonic]
    return binary

def comp(mnemonic):
    c1toc6, abit = compTable[mnemonic]
    binary = abit + c1toc6
    return binary

print dest('AMD')

print comp('D-1')
    

