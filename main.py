import storageHandler as sh
from record import *
from node import *
import re

if __name__ == "__main__":

    sh.initialize()

    records = []
    for block in sh.fetchNextBlock():
        blockRecords = Record.parseXMLToRecordsList(block)
        records.extend(blockRecords)
        sh.storeRecordList(blockRecords)


    # print(records)

    for i in range(1, sh.getBlockNumber(DATAFILE)):
        print(sh.fetchBlock(DATAFILE, i))

    #for record in records:
   #     print(record)
    #     sh.storeRecord(record)

   # print(RECORD_SIZE, NODE_SIZE)

    print(sh.fetchBlock(DATAFILE,1))