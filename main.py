import Record
import storageHandler as sh
from Record import *
from RTreeNode import *
from RStarTree import RStarTree

if __name__ == "__main__":

    sh.initialize()

    sh.storeRecord(Record(Point("dummy","0",["1.0" for _ in range(NUM_OF_COORDINATES)])))

    # print(RECORD_SIZE)

    records = []
    for block in sh.fetchNextBlock():
        blockRecords = Record.parseXMLToRecordsList(block)
        records.extend(blockRecords)
        sh.storeRecordList(blockRecords)


    block = sh.fetchBlock(DATAFILE,1)
    for r in block:
        print(RTreeEntry(data = r))



