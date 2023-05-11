from record import Record
from config import *
import re
from time import time

def initialize():

    files = (DATAFILE, INDEXFILE)

    for file in files:
        cursor = open(file, "ab+")
        # Getting the end of the file
        cursor.seek(0, 2) # get to the end of file
        
        fileOccupancy = cursor.tell()

        # Check if the file is empty or badly initialised
        if fileOccupancy < BLOCKSIZE:
            
            # prepare a block of data to write
            initBlock = [0 for _ in range(BLOCKSIZE)]
            initHeader = FILEHEADER.format(file)

            # combine the two
            for i in range(len(initHeader)):
                initBlock[i] = ord(initHeader[i].encode('utf-8'))
            
            # convert to byte array
            initBlock = bytearray(initBlock)

            # write to file
            cursor.close()
            cursor = open(file, "wb+")
            cursor.seek(0)
            cursor.write(initBlock)
        
        cursor.close()
            

def fetchNextBlock(test = True):
    with open(INPUTFILE, "rb") as file:
        remnants = ""

        filesize = file.seek(0, 2)
        file.seek(0)
        while file.tell() < filesize-BLOCKSIZE:
            inText = file.read(BLOCKSIZE).decode('utf-8')
            block = remnants + inText
            remnants = block[-2000:]

            yield block
        else:
            inText = file.read(filesize - file.tell()).decode('utf-8')
            block = remnants + inText
            yield block


records = 0
latestBlock = 1
blockEnd = 0

#TODO: COMMENTS AND CLEANUP!!!
def storeRecord(record: Record):
    global blockEnd, records, latestBlock

    with open(DATAFILE, "rb+") as cursor:

        cursor.seek(0, 2)

        end = cursor.tell()

        newBlock = [0]*BLOCKSIZE

        if end//BLOCKSIZE == 1:
            cursor.write(bytearray(newBlock))


        cursor.seek(latestBlock*BLOCKSIZE)
        currentBlock = bytearray(cursor.read(BLOCKSIZE))

        # Check if record fits in block
        if not blockEnd + len(str(record)) >= BLOCKSIZE:
            for i, byte in enumerate(bytearray(str(record).encode("utf-8"))):
                currentBlock[blockEnd+i] = byte

            blockEnd += len(bytearray(str(record).encode("utf-8")))

        else:
            latestBlock+=1
            blockEnd = 0
            currentBlock = newBlock
            for i, byte in enumerate(bytearray(str(record).encode("utf-8"))):
                currentBlock[blockEnd + i] = byte

            blockEnd += len(bytearray(str(record).encode("utf-8")))

        cursor.seek(latestBlock * BLOCKSIZE)
        cursor.write(currentBlock)
        records =+ 1

        return latestBlock, blockEnd//len(bytearray(str(record).encode("utf-8")))

