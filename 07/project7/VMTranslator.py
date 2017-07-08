import logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from VMUtils import *
import VMParser
import VMCodeWriter

# Get VM Files in current folder

VMFiles = find_in_folder('vm')
logger.info('Found the following files: %s' % VMFiles)

# For each file do these steps
for item in VMFiles:
    logger.info('Processing %s' % item)
    
    parsed = VMParser.process(item)

    if parsed:
        logger.info('Successfully parsed %s' % item)
        
    # Write machine code        
    code = VMCodeWriter.code(parsed)
    
    # Save to new file
    newFileName = change_extension(item, 'asm')
    saveFile(code, newFileName)
    

    


