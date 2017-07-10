# Storing of translation pairs in dictionaries
# Should look into either xml or yaml for storing this data in a
# human readable/writeable settings format

commandTypes = {
                'add'           :       'C_ARITHMETIC'  ,
                'sub'           :       'C_ARITHMETIC'  ,
                'neg'           :       'C_ARITHMETIC'  ,
                'eq'            :       'C_ARITHMETIC'  ,
                'gt'            :       'C_ARITHMETIC'  ,
                'lt'            :       'C_ARITHMETIC'  ,
                'and'           :       'C_ARITHMETIC'  ,
                'or'            :       'C_ARITHMETIC'  ,
                'not'           :       'C_ARITHMETIC'  ,                
                'push'          :       'C_PUSH'        ,
                'pop'           :       'C_POP'         ,
                'label'         :       'C_LABEL'       ,
                'goto'          :       'C_GOTO'        ,
                'if'            :       'C_IF'          ,
                'function'      :       'C_FUNCTION'    ,
                'return'        :       'C_RETURN'      ,
                'call'          :       'C_CALL'         
               }

# 1 BINARY 0 UNARY -1 JMP

aCommands =    {
                'add'           :       [1  , '+'] ,
                'sub'           :       [1  , '-'] ,
                'neg'           :       [0  , '-'] , 
                'eq'            :       [-1 , 'JEQ'] ,
                'gt'            :       [-1 , 'JGT'] ,
                'lt'            :       [-1 , 'JLT'] ,
                'and'           :       [1  , '&'] ,
                'or'            :       [1  , '|'] ,
                'not'           :       [0  , '!']    
                }

memSegments = {    
               'local'          :       'LCL'  ,
               'argument'       :       'ARG'  ,
               'this'           :       'THIS' ,
               'that'           :       'THAT'     
              }
'''
null No jump
JGT If out > 0 jump
JEQ If out ? 0 jump
JGE If out b 0 jump
JLT If out < 0 jump
JNE If out 0 0 jump
JLE If out a 0 jump
JMP

add
sub
neg
eq
gt
lt
and
or
not
'''