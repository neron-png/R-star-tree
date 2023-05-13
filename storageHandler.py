import record
from record import *
from node import *
from config import *
import re
from time import time

totalRecords = 0
latestBlock = 1
blockEnd = 0

def getBlockNumber(file):
    if file == DATAFILE:
        return latestBlock
    else:
        return None #TODO

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



def storeRecordList(recordsList: list):
    global blockEnd, totalRecords, latestBlock
    # Opening the file in read-bytes + (write) mode
    with open(DATAFILE, "rb+") as cursor:

        #################
        # SETTING IT UP #
        #################

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

        #######################
        # HANDING THE RECORDS #
        #######################

        for record in recordsList:

            # CHECK IF WE NEED TO MAKE MORE SPACE IN THE FILE
            if not blockEnd + RECORD_SIZE < BLOCKSIZE:
                # Oop, we're in a new block, let's write the old one
                cursor.seek(latestBlock * BLOCKSIZE)
                cursor.write(currentBlock)

                currentBlock = newBlock
                blockEnd = 0
                latestBlock += 1

            ################

            # UPDATING THE RECORD'S INFORMATION
            record.slotId = totalRecords - ((latestBlock-1)*(BLOCKSIZE//RECORD_SIZE))
            record.blockId = latestBlock

            # Converting said record into bytes
            recordData = bytearray(str(record).encode("utf-8"))
            totalRecords += 1

            # Appending the record's bytes into the block data
            for i, byte in enumerate(recordData):
                currentBlock[blockEnd + i] = byte
            # print(blockEnd)
            blockEnd += RECORD_SIZE

        else:
            # Storing the block at the end of the loop
            cursor.seek(latestBlock * BLOCKSIZE)
            cursor.write(currentBlock)






#TODO: COMMENTS AND CLEANUP!!!
def storeRecord(record: Record):

    storeRecordList([record])


#HELLO PAL!
def fetchBlock(filename, blockId: int) -> list:
    if filename == DATAFILE:
        offset = RECORD_SIZE
    elif filename == INDEXFILE:
        offset = NODE_SIZE
    else:
        return None

    with open(filename, "rb+") as file:

        # Seek to the block start
        file.seek(BLOCKSIZE * blockId)

        # Read the block's bytes
        blockBytes = file.read(BLOCKSIZE)

        # Remove the trailing null characters and convert to string
        block = blockBytes[:-1*blockBytes.count(0)].decode('utf-8')

        if filename == DATAFILE:
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
        target = BLOCKSIZE*blockid

        emptyness = end - target

        if emptyness > 0:
            fillerBlock = bytearray([0] * emptyness)
            cursor.write(fillerBlock)

        cursor.seek(BLOCKSIZE*blockid)

        newBlock = bytearray([0] * BLOCKSIZE)

        blockBytes = bytearray("".join([str(record) for record in block]).encode("utf-8"))

        if len(blockBytes) > BLOCKSIZE:
            raise f"Error: Trying to write a block list that's larger than BLOCKSIZE ({BLOCKSIZE})"

        for i, newByte in enumerate(blockBytes):
            newBlock[i] = newByte
        
        cursor.write(newBlock)
        
                      