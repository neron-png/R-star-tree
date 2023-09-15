import itertools
from RTree import Rtree
from Record import Record
import StorageHandler
import RTReeUtil
import config
from time import time

if __name__ == "__main__":
    
    StorageHandler.writeBlocksToDatafile()

    parseData = RTReeUtil.parseDataJson() #len = 8308
    dataTree = Rtree()
    dataTree.bottom_up(parseData)
    
    range = [[41.4259*config.MANTISSA, 26.3911*config.MANTISSA],
             [41.984*config.MANTISSA, 26.5524*config.MANTISSA]]
    range2 = [[41.4259, 26.3911],
             [41.984, 26.5524]]
    
    range = [[41.1259*config.MANTISSA, 26.1911*config.MANTISSA],
             [41.984*config.MANTISSA, 26.5524*config.MANTISSA]]
    range2 = [[41.1259, 26.1911],
             [42.184, 26.9524]]
    

    start = time()
    results = []

    for i in itertools.count(start=1):

        try:
            block = StorageHandler.getBlockFromDisk(i)
            for record in block["slots"]:
                if RTReeUtil.inRectangle(record["coords"], range):
                    results.append(record)

        except Exception as e:
            break
    duration = time() - start
    print(f"Serial search range query: {int(1000*(duration))}ms")

    start = time()
    results2 = dataTree.rangeQuery(range2)
    duration = time() - start
    print(f"R-Tree range query: {int(1000*(duration))}ms")