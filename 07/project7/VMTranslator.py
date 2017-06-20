import logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from VMUtils import *
import VMParser

def process(file):
    
    logger.info('Load VM File into memory')
    
    fileContent = loadFile(file)
    
    # Parse it
          
    for line in fileContent:
        removed_comments = remove_comments(line)
        parsed = VMParser.parse(removed_comments)
        if removed_comments != False:
            logger.debug(parsed)
    
    # Write machine code
    
    # Save to new file    
    
    

# Get VM Files in current folder

VMFiles = find_in_folder('vm')
logger.info('Found the following files: %s' % VMFiles)

# For each file do these steps
for item in VMFiles:
    logger.info('Processing %s' % item)
    process(item)


