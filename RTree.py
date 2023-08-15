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
        self.m = int(config.m*self.nodeCap)
        """
        nodes = [{"id": 1, "level":0, "type": n, "rectangle" = []}, ...]
        nodes_ = {"root": {"id": 0, "level": 0},
                    1: {"id": 1, "level":0, "type": n, "rectangle" = []}...}
        """
        if indexfile is not None:            
            with open(config.INDEXFILE, "r") as f:
                self.nodes_ = json.load(f, object_hook=RTReeUtil.intObjectHook)
                
    def rangeQuery(self, corners: list) -> list:
        """
        :param corners: ist of (n-1)-d rectangle's corners (floats)
        :return: list of records (points) included in the rectangle 
        """

        if len(corners) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of points for a " + str(config.NUM_OF_COORDINATES) + "-D rectangle.")

        # Get the list of pointers in datafile for the points corresponding to the range query
        result = Queries.rangeQuery(self.nodes_, self.nodes_["root"]["id"], [[int(corner[axis] * config.MANTISSA) for axis in range(len(corner))] for _, corner in enumerate(corners)])
        
        records = []

        # For each datafile-point, fetch the actual record
        for pointer in result:
            record = StorageHandler.fetchRecordFromDisk(pointer["bID"], pointer["sIndex"])
            record.pop("_")
            record["coords"] = [c / config.MANTISSA for c in record["coords"]]
            records.append(record)
        
        return records
    
    def skylineQuery(self) -> list:
        return []

    
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

    
    def insert(self, record: dict|None):
        """
        :param Record dict: {
                            "bID": int,
                            "sID": int,
                            "coords": list [x, y, z...]
                            }
        :return: None, adds node to tree
        """
        from RTReeInsert.Insert import insertData
        self.nodes_ = insertData(nodeCap=self.nodeCap, m=self.m, nodes=self.nodes_, record={"coords": [413672865000, 261587581000], "name":"Cousgo"})
        
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
    # print(tempTree.rangeQuery([[41.5,26.5],[42.1,26.52]]))
    # # StorageHandler.writeRtreeToFile(tempTree.nodes_)
    tempTree.insert(None)
    # tempTree.delete(301073184)
    StorageHandler.writeRtreeToFile(tempTree.nodes_)
