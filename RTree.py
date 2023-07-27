import RTReeUtil
from Record import Record
import config
import json
import StorageHandler
import Queries


class Rtree():

    def __init__(self, indexfile=None):
        self.nodeCap: int = config.BLOCKSIZE // config.ENTRYSIZE
        self.nodes = []

        if indexfile is not None:            
            with open(config.INDEXFILE, "r") as f:
                self.nodes = json.load(f)


    def rangeQuery(self, corners: list) -> list:
        if len(corners) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of points for a " + str(config.NUM_OF_COORDINATES) + "-D rectangle.")

        return Queries.rangeQuery(self, self.nodes[-1], [[int(corner[axis] * config.MANTISSA) for axis in range(len(corner))] for _, corner in enumerate(corners)])

    
    def bottom_up(self, points):
        """
        :param points: list of simple point coordinates 
            [{"bID": int,
            "sIndex": int,
            "coords": [x, y]}
            , ...
        :return: None, fills up the self.nodes as a flat list
        """
        from RTReeBulkload import bottom_up
        self.nodes = bottom_up(self.nodeCap, self.nodes, points)

    
    def insert(self, record: dict):
        """
        :param Record dict: {
                            "bID": int,
                            "sID": int,
                            "coords": list [x, y, z...]
                            }
        :return: None, adds node to tree
        """
        from RTreeInsert import insert
        self.nodes = insert(self.nodeCap, self.nodes, record)
        

    def delete(self, id):
        import RTReeDelete
        RTReeDelete.delete(self.nodes, self.nodeCap, id)




def run():

    parseData = RTReeUtil.parseDataJson()
    tempTree = Rtree(config.INDEXFILE)
    # tempTree = Rtree()
    # print(tempTree.rangeQuery([[41.5,26.5],[42.1,26.52]]))
    # tempTree.bottom_up(parseData)
    # StorageHandler.writeRtreeToFile(tempTree.nodes)
    tempTree.insert()
    # tempTree.delete(301073184)
    # StorageHandler.writeRtreeToFile(tempTree.nodes)
