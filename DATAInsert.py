from RTree import Rtree
from Record import Record
import StorageHandler
import RTReeUtil
import config
from time import time

if __name__ == "__main__":

    StorageHandler.writeBlocksToDatafile()
    dataTree = Rtree()

    parseData = RTReeUtil.parseDataJson() #len = 8308
    
    datasets = (1000, 2000, 3500, 4000)
    print("Consecutive inserts:")
    for size in datasets:
        dataSet = parseData[:size]
        start = time()
        for item in dataSet:
            dataTree.insert(Record(id=item["sIndex"], coords=item["coords"], name="inserted"))
            
            
        StorageHandler.writeRtreeToFile(dataTree.nodes)
        end = time()
        print(f"{size}: {int(1000*(end-start))}ms")
    
    
    StorageHandler.writeBlocksToDatafile()
    dataTree = Rtree()
    parseData = RTReeUtil.parseDataJson() #len = 8308
    print("Bulk loading:")
    for size in datasets:
        dataSet = parseData[:size]
        
        start = time()
        dataTree.bottom_up(dataSet)
        StorageHandler.writeRtreeToFile(dataTree.nodes)
        end = time()
        print(f"{size}: {int(1000*(end-start))}ms")

