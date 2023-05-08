import storageHandler as sh
from record import *


records = []
for block in sh.fetchNextBlock():
    records.append(Record.parseXMLtoRecordsList(block))

print(records)

sh.initialize()

sh.storeRecord(None)