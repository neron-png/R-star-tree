import RTReeUtil
import config
from RTReeUtil import zOrder
import json
from pprint import pprint  # FIXME debug
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

        if len(corners) != len(self.nodes[-1]) or len(corners) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of points for a " + config.NUM_OF_COORDINATES + "-D rectangle.")
        
        return Queries.rangeQuery(self.nodes[-1],[c * config.MANTISSA for c in corners])

    
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


    def delete(self, id):
        import deleteTemp
        deleteTemp.delete(self.nodes, self.nodeCap, id)




def parseDataJson():
    """
        Parsing the fully formatted Json into a list of coordinates and record IDs ready to be
        parsed into the bottom up place.
    """
    sample = []
    import json
    with open(config.DATAFILE, "r") as f:
        sample = json.load(f)

    parsedSample = []
    for block in sample:
        for i, item in enumerate(block["slots"]): 
            parsedItem =    {
                                "bID": block["id"],
                                "sIndex": i,
                                "coords": item["coords"]
                            }
            parsedSample.append( parsedItem )

    return parsedSample


def run():

    # coords = decimalise(float_coords)
    parseData = parseDataJson()
    tempTree = Rtree()
    tempTree.bottom_up(parseData)
    StorageHandler.writeRtreeToFile(tempTree.nodes)
    tempTree.delete(301073184)
    # StorageHandler.writeRtreeToFile(tempTree.nodes)
