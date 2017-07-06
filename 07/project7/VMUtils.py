'''
VMUtils
'''
import os

def loadFile(filepath):
    
    lines = []
    
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n\r') for line in f if line != '\n']

        return lines
    
def change_extension(filepath, new):
    
    extension = filepath.split('.')[-1]
    filepath = filepath.replace(extension,new)
    
    return filepath
    
def saveFile(datafile, filepath):
    
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

def find_in_folder(searchterm):
    '''Returns files in current folder that include search term'''
    currentFile = __file__
    currentDir = os.path.dirname(currentFile)
    filelist = os.listdir(currentDir)
    result = [os.path.join(currentDir,x) for x in filelist if searchterm in x]
    
    return result
    
