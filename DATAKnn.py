from RTree import Rtree
from Record import Record
import StorageHandler
import RTReeUtil
import config
from time import time

if __name__ == "__main__":

    StorageHandler.writeBlocksToDatafile()
    parsedData = RTReeUtil.parseDataJson()
    
    tree = Rtree()
    tree.bottom_up(parsedData)

    
    point = [41.425, 26.3910]
    kSet = (5, 10, 25, 100, 150)

    for k in kSet:
        start = time()
        tree.nearestNeighborsQuery(point, k)
        end = time()
        print(f"k={k}: {int(1000*(end-start))}ms")
    

    for k in kSet:
        i = 1
        while True:
            block = StorageHandler.getBlockFromDisk(i)
            for record in block["slots"]:
                    


            i += 1
    