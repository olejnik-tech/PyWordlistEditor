import Properties
#for listdir
import os
#for regex
import re
import datetime
from datetime import datetime, date

def readTxtFileNames():
    files = os.listdir(Properties.path)
    result = []
    print("txt files in directory:")
    for name in files:
        if re.search("(.*\.txt)", name):
            result.append(Properties.path+name)
            print (Properties.path+name)
    return result

def processAllFiles():

    # Managing output file
    # This process might be unnecessary, just open and close on the moment of writing. ???
    # read first then append, is that possible???
    # read can be closed as well ... it is starting from beginning anyway

    # flags and counters
    cache = []
    cacheInvalid = []
    prevTime = datetime.now().time()
    duplicateCounter = 0
    lowCounter = 0
    highCounter = 0
    writtenCounter = 0
    totalCounter = 0

    outputFile = open(Properties.outputFile,"a")
    outputFile.close()

    files = readTxtFileNames()

    # BROWSE INPUT FILES
    for file in files:
        f  = open(file, "r")

        # BROWSE ONE LINE OF FILE
        for line in f:

            totalCounter += 1
            if("\n" not in line):
                line = line + "\n"
            
    # <<<<          ----- VALIDATION -----          >>>>
            valid = True

            # line < 8
            if(len(line) < 8):
                valid = False
                lowCounter += 1

            elif(len(line) > 16):   
                valid = False
                highCounter += 1

            elif(line in cache):
                valid = False
                duplicateCounter +=1

            # duplicates (opening outputFile for second time just with read access to browse and compare)
            else:
                outputFileforMerge = open(Properties.outputFile,"r")
                for lineOutput in outputFileforMerge:

                    if(lineOutput == line):
                        valid = False
                        duplicateCounter += 1
                        
                outputFileforMerge.close()

            if(valid):
                cache.append(line)

                if(len(cache) > Properties.buffer -1):
                    newFile = open(Properties.outputFile,"a")
                    for cacheLine in cache:
                        newFile.write(cacheLine)
                        writtenCounter += 1
                    newFile.close()
                    cache = []
                    print(">>> " + str(Properties.buffer) + " records in: " + str(datetime.combine(datetime.today(), datetime.now().time()) - datetime.combine(datetime.today(), prevTime)) + " non-valid: " + str(duplicateCounter+lowCounter+highCounter) + " written lines: " + str(writtenCounter) + " total: " + str(totalCounter))
                    print(">>> duplicates: " + str(duplicateCounter))
                    print(">>> examples of invalid records:\n" + cacheInvalid[0] + cacheInvalid[1] + cacheInvalid[2] + cacheInvalid[3] + cacheInvalid[4])
                    cacheInvalid=[]
                    prevTime = datetime.now().time()
            elif(len(cacheInvalid) < 5):
                cacheInvalid.append(line)
                    
                
        f.close()

    print(">>> duplicate records: " + str(duplicateCounter))
    print(">>> too low records: " + str(lowCounter))
    print(">>> too high records: " + str(highCounter))
    print(">>> written records: " + str(writtenCounter))
    print("----- closing output file -----")

processAllFiles()