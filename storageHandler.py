# from record import Record
from config import *


def initialize():

    files = (DATAFILE, INDEXFILE)

    for file in files:
        with open(file, "ab+") as cursor:
            cursor.seek(0, 2)
            print(cursor.tell())


def fetchNextBlock():
    with open(INPUTFILE, "rb") as file:
        yield file.read(BLOCKSIZE)


records = 0
latestBlock = 1
blockEnd = 0

# def storeRecord(record: Record):


