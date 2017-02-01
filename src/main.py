'''
Created on Jan 30, 2017
@author: Subhasis
'''

import sys
from datetime import datetime

from FileParserService import FileParserService

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())
    inputFile = sys.argv[1]
    processor = FileParserService(inputFile)

    processComplete = processor.process()

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())
