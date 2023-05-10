import storageHandler as sh
from record import *
import re

if __name__ == "__main__":

    records = []
    for block in sh.fetchNextBlock():
        blockRecords = Record.parseXMLtoRecordsList(block)
        records.extend(Record.parseXMLtoRecordsList(block))


    print(records)
    sh.initialize()

    sh.storeRecord(None)