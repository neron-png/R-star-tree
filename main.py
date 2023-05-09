import storageHandler as sh
from record import *
import re


records = []
with open("test.xml", "w+", encoding="utf-8") as f:
    for block in sh.fetchNextBlock():
        print(block)
        # print("nodes:",nodes)
        # print("block:",block)
        # records.append(Record.parseXMLtoRecordsList(block))

print(records)

sh.initialize()

sh.storeRecord(None)