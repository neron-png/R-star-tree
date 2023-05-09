from record import Record
from config import *
import re


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
            

def fetchNextBlock():
    with open(INPUTFILE, "rb") as file:
        remnants = ""
        pattern = r"(<node.*/>)|(<node.*>(\n|\b|.)*<\/node>)"

        filesize = file.seek(0, 2)
        file.seek(0)
        while file.tell() < filesize-BLOCKSIZE:
            block = remnants + file.read(BLOCKSIZE).decode('utf-8')

            nodes = ["".join(x) for x in re.findall(pattern, block)]
            for node in nodes:
                block.replace(node, '')
            remnants = block

            yield "".join(nodes)
        else:
            yield remnants + file.read(filesize - file.tell()).decode('utf-8')


records = 0
latestBlock = 1
blockEnd = 0

def storeRecord(record: Record):

    with open(DATAFILE, "rb+") as cursor:

        cursor.seek(0, 2)
        print(cursor.tell())

        end = cursor.tell()
        if end//BLOCKSIZE:
            pass

