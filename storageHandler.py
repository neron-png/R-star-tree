# from record import Record
from config import *


def initialize():

    files = (DATAFILE, INDEXFILE)

    for file in files:
        cursor = open(file, "ab+")
        # Getting the end of the file
        cursor.seek(0, 2) # get to the end of file
        
        fileOccupancy = cursor.tell()

        if fileOccupancy < BLOCKSIZE:
            
            initBlock = [0 for _ in range(BLOCKSIZE)]
            initHeader = FILEHEADER.format(file)

            for i in range(len(initHeader)):
                initBlock[i] = initHeader[i]

            initBlock = bytearray(initBlock)

            cursor.close()
            cursor = open(file, "wb+")
            cursor.seek(0)
            cursor.write(initBlock)
        
        cursor.close()
            

def fetchNextBlock():
    with open(INPUTFILE, "rb") as file:
        yield file.read(BLOCKSIZE).decode('utf-8')


records = 0
latestBlock = 1
blockEnd = 0

# def storeRecord(record: Record):


