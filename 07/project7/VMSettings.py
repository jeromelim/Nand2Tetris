
commandTypes = {'add'           :       'C_ARITHMETIC'  ,
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

aCommands =    {'add'           :       'C_ARITHMETIC'  ,
                'sub'           :       'C_ARITHMETIC'  ,
                'neg'           :       'C_ARITHMETIC'  ,
                'eq'            :       'JEQ'  ,
                'gt'            :       'JGT'  ,
                'lt'            :       'JLT'  ,
                'and'           :       'C_ARITHMETIC'  ,
                'or'            :       'C_ARITHMETIC'  ,
                'not'           :       'C_ARITHMETIC'  

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