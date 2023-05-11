import storageHandler as sh
from record import *
from node import *
import re

if __name__ == "__main__":

    sh.initialize()

    records = []
    for block in sh.fetchNextBlock():
        blockRecords = Record.parseXMLtoRecordsList(block)
        records.extend(blockRecords)
        sh.storeRecordList(blockRecords)


    # print(records)


    for record in records:
        print(record)
    #     sh.storeRecord(record)

    print(RECORD_SIZE, NODE_SIZE)