from RTree import Rtree
from Record import Record
import StorageHandler
import RTReeUtil


if __name__ == "__main__":

    ''' Bulk loading '''
    StorageHandler.writeBlocksToDatafile()
    parsedData = RTReeUtil.parseDataJson()
    
    tree = Rtree()
    tree.bottom_up(parsedData)

    StorageHandler.writeRtreeToFile(tree.nodes)


    ''' R*-Tree Operations'''
    r = Record(id=1201029, coords=[41.3672865000, 26.1587581000], name="Cousgo")
    tree.insert(record=r)
    tree.delete(id=301073184)

    StorageHandler.writeRtreeToFile(tree.nodes)

    ''' Queries '''
    range = [[41.5, 26.5],[42.1, 26.52]]
    rangeQueryResults = tree.rangeQuery(corners=range)
    print(rangeQueryResults)
   
    skylineQueryResults = tree.skylineQuery()
    print(skylineQueryResults)

    knnQueryResults = tree.nearestNeighborsQuery(queryPoint=[41.47, 26.16], k=100)
    print(knnQueryResults)

