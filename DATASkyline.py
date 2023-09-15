from RTree import Rtree
from Record import Record
import StorageHandler
import RTReeUtil

from time import time

if __name__ == "__main__":

    StorageHandler.writeBlocksToDatafile()
    parsedData = RTReeUtil.parseDataJson()
    
    tree = Rtree()
    
    for size in (1000, 2000, 3200, 4000):
        dataSet = parsedData[:size]
        tree.bottom_up(parsedData)
        from StorageHandler import writeRtreeToFile
        writeRtreeToFile(tree.nodes)
        start = time()
        tree.skylineQuery() 
        end = time()
        print(f"{int(1000*(end-start))}ms")


            
    