from record import *
from node import *
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


totalRecords = 0
latestBlock = 1
blockEnd = 0

def storeRecordList(recordsList: list):
    global blockEnd, totalRecords, latestBlock
    # Opening the file in read-bytes + (write) mode
    with open(DATAFILE, "rb+") as cursor:

        # Getting to the end of the file
        cursor.seek(0, 2)
        end = cursor.tell()

        # Pre-initialising an emtpy block to write for padding
        newBlock = bytearray([0] * BLOCKSIZE)

        # If it's the first commit, we're writing the empty block
        if end // BLOCKSIZE == 1:
            cursor.write(bytearray(newBlock))

        # Seeking to the latest block and reading it to append the new data
        cursor.seek(latestBlock * BLOCKSIZE)
        currentBlock = bytearray(cursor.read(BLOCKSIZE))

        for record in recordsList:
            recordData = bytearray(str(record).encode("utf-8"))
            recordSize = len(recordData)

            if not blockEnd + recordSize < BLOCKSIZE:
                # Oop, we're in a new block, let's write the old one
                cursor.seek(latestBlock * BLOCKSIZE)
                cursor.write(currentBlock)

                currentBlock = newBlock
                blockEnd = 0
                latestBlock += 1

            totalRecords += 1
            # TODO: add the coords to the record and update recordData
            for i, byte in enumerate(recordData):
                currentBlock[blockEnd + i] = byte
            blockEnd += recordSize

        else:
            cursor.seek(latestBlock * BLOCKSIZE)
            cursor.write(currentBlock)






#TODO: COMMENTS AND CLEANUP!!!
def storeRecord(record: Record):

    storeRecordList([record])


#HELLO PAL!
def fetchBlock(file, blockId: int) -> list:
    if file == DATAFILE:
        offset = RECORD_SIZE
    elif file == INDEXFILE:
        offset = NODE_SIZE
    else:
        return None

    with open(file, "rb") as file:
        file.seek(0)
        file.seek(offset * blockId)
        block = file.read(BLOCKSIZE).decode('utf-8')

    if file == DATAFILE:
        return Record.parseBlockToRecordsList(block)
    else:
        # return Node.parseBlockToNodeList(block)
        pass


#TODO: EVERYTHING
def storeBlock(block: list, blockid: int):
    global blockEnd, totalRecords, latestBlock
    # Opening the file in read-bytes + (write) mode
    with open(INDEXFILE, "rb+") as cursor:

        # Getting to the end of the file
        cursor.seek(0, 2)
        end = cursor.tell()
        cursor.seek(BLOCKSIZE*blockid)

        blockBytes = bytearray([str(record).encode('utf-8') for record in block])
        
        cursor.write(blockBytes)
        
                      