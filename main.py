from RTree import Rtree
from Record import Record
import StorageHandler
import RTReeUtil
import config

if __name__ == "__main__":

    StorageHandler.write_blocks_to_datafile()
    # tempTree = Rtree(config.INDEXFILE)
    tempTree = Rtree()

    # r = Record(id=32, coords=[1,2], name="Greece")
    # StorageHandler.writeRecordToDisk(r)
    # StorageHandler.deleteRecordFromDisk(2781,32)

    parseData = RTReeUtil.parseDataJson()
    tempTree.bottom_up(parseData)
    # print(tempTree.rangeQuery([[41.5,26.5],[42.1,26.52]]))
    # # StorageHandler.writeRtreeToFile(tempTree.nodes_)
    # pprint(tempTree.nodes[0])
    # tempTree.insert(Record(id=1201029, coords=[41.3672865000, 26.1587581000], name="Cousgo"))
    # tempTree.delete(id=1201029)
    # tempTree.insert(None)
    # tempTree.delete(301073184)
    StorageHandler.writeRtreeToFile(tempTree.nodes)
    # print(tempTree.skylineQuery())

