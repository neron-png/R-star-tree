from pprint import pprint
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
        self.nodes_ = {"root": {"id": 0, "level": 0}}
        """
        nodes = [{"id": 1, "level":0, "type": n, "rectangle" = []}, ...]
        nodes_ = {"root": {"id": 0, "level": 0},
                    1: {"id": 1, "level":0, "type": n, "rectangle" = []}...}
        """
        #TODO: Update to nodes_
        if indexfile is not None:            
            with open(config.INDEXFILE, "r") as f:
                self.nodes_ = self.nodes = json.load(f, object_hook=RTReeUtil.intObjectHook)
                
    #TODO: Update to nodes_
    def rangeQuery(self, corners: list) -> list:
        if len(corners) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of points for a " + str(config.NUM_OF_COORDINATES) + "-D rectangle.")

        return Queries.rangeQuery(self.nodes_, self.nodes_["root"]["id"], [[int(corner[axis] * config.MANTISSA) for axis in range(len(corner))] for _, corner in enumerate(corners)])

    
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
        self.nodes_ = bottom_up(self.nodeCap, self.nodes_, points)

    
    #TODO: Update to nodes_
    def insert(self, record: dict|None):
        """
        :param Record dict: {
                            "bID": int,
                            "sID": int,
                            "coords": list [x, y, z...]
                            }
        :return: None, adds node to tree
        """
        from RTreeInsert import insert
        self.nodes_ = insert(self.nodeCap, self.nodes_, [413672865000, 261587581000])
        
    #TODO: Update to nodes_
    def delete(self, id):
        import RTReeDelete
        RTReeDelete.delete(self.nodes_, self.nodeCap, id)




def run():

    parseData = RTReeUtil.parseDataJson()
    # tempTree = Rtree(config.INDEXFILE)
    tempTree = Rtree()
    
    # r = Record(id=32, coords=[1,2], name="Greece")
    # StorageHandler.writeRecordToDisk(r)
    # StorageHandler.deleteRecordFromDisk(2781,32)

    tempTree.bottom_up(parseData)
    print(tempTree.rangeQuery([[41.5,26.5],[42.1,26.52]]))
    StorageHandler.writeRtreeToFile(tempTree.nodes_)
    tempTree.insert(None)
    # tempTree.delete(301073184)
    StorageHandler.writeRtreeToFile(tempTree.nodes_)
