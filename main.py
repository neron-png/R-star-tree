import record
import storageHandler as sh
from record import *
from node import *
from RTree import RTree

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

    # for i in range(1, sh.getBlockNumber(DATAFILE)+1):
    # for i in range(1, 54):
    #     recordFile = sh.fetchBlock(DATAFILE, i)
    #     for record in sh.fetchBlock(DATAFILE, i):
    #         print(str(record))


    rtree = RTree()


