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
        self.nodes = {"root": {"id": 0, "level": 0, "first_insert": True}}#, "0": {"id": 0, "type": "l", "level": 0, "records": [], "rectangle": [[0, 0], [1, 1]]}}
        self.m = int(config.m*self.nodeCap)
        """
        nodes = {"root": {"id": 0, "level": 0},
                    1: {"id": 1, "level":0, "type": n, "rectangle" = []}...}
        """
        if indexfile is not None:
            with open(config.INDEXFILE, "r") as f:
                self.nodes = json.load(f, object_hook=RTReeUtil.intObjectHook)

    def rangeQuery(self, corners: list) -> list:
        """
        :param corners: ist of (n-1)-d rectangle's corners (floats)
        :return: list of records (points) included in the rectangle
        """
        if len(corners) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of points for a " + str(config.NUM_OF_COORDINATES) + "-D rectangle.")

        return Queries.rangeQuery(self.nodes, self.nodes["root"]["id"],
                                  [[int(corner[axis] * config.MANTISSA) for axis in range(len(corner))] for _, corner in enumerate(corners)])

    def skylineQuery(self) -> list:
        return Queries.skylineQuery(self.nodes)

    def nearestNeighborsQuery(self, queryPoint: list, k: int):
        if len(queryPoint) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of coordinates for a " + str(config.NUM_OF_COORDINATES) + "-D point.")
        
        return [o[0] for o in Queries.nearestNeighborsQuery(self.nodes, self.nodes[self.nodes["root"]["id"]], [c * config.MANTISSA for c in queryPoint], k, [])]


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


    def insert(self, record: Record):
        """
        :param Record Record
        :return: None, adds node to tree
        """
        # if record == None:
            # record=Record(id=1201029, coords=[41.3672865000, 26.1587581000], name="Cousgo")
        from RTReeInsert.Insert import insertData
        insertData(nodeCap=self.nodeCap, m=self.m, nodes=self.nodes, record=record)


    def delete(self, id):
        import RTReeDelete
        RTReeDelete.delete(nodes=self.nodes, nodeCap= self.nodeCap, id=id, m=self.m)
