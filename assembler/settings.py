#filepath = r'C:\Users\Jerome\Documents\GitHub\hackassembler\data\add\Add.asm'
import os
import __main__

currentdir = os.path.dirname(__file__)
rootdir = currentdir.replace('\\assembler', '')

#inputpath = r'data\add\Add.asm'
#inputpath = r'data\max\Max.asm'
#inputpath = r'data\pong\Pong.asm'
inputpath = r'data\rect\Rect.asm'
filepath = os.path.join(rootdir, inputpath)
outputpath = r'output'
savepath =  os.path.join(rootdir, outputpath)

# Grammar

remove_all_after = [
                    r'//'
                   ]

remove_all = [
          '\r\n',
          '\n'
]


