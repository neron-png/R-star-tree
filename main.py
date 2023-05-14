import record
import storageHandler as sh
from record import *
from node import *
import re

if __name__ == "__main__":

    sh.initialize()

    sh.storeRecord(Record(Point("dummy","0",["1.0" for _ in range(NUM_OF_COORDINATES)])))

    print(RECORD_SIZE)

    records = []
    for block in sh.fetchNextBlock():
        blockRecords = Record.parseXMLToRecordsList(block)
        records.extend(blockRecords)
        sh.storeRecordList(blockRecords)


    # print(records)

    for i in range(1, sh.getBlockNumber(DATAFILE)):
        for record in sh.fetchBlock(DATAFILE, i):
            pass
            # record.slotId = 1
            # print("record.blockId: ", record.blockId)
            # print("record.slotId: ", record.slotId)
            # print(str(record))

    #for record in records:
   #     print(record)
    #     sh.storeRecord(record)

   # print(RECORD_SIZE, NODE_SIZE)

    for r in sh.fetchBlock(DATAFILE,2):
        print(r)

