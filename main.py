import storageHandler as sh
from record import *
import re

if __name__ == "__main__":

    sh.initialize()

    records = []
    for block in sh.fetchNextBlock():
        blockRecords = Record.parseXMLtoRecordsList(block)
        records.extend(blockRecords)


    print(records)


    for record in records:
        sh.storeRecord(record)
