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

        if len(corners) != config.NUM_OF_COORDINATES:
            raise Exception("Provide the exact minumum amount of points for a " + config.NUM_OF_COORDINATES + "-D rectangle.")
        
        return Queries.rangeQuery(self.nodes[-1], corners)

    def bottom_up(self, points):
        """
        :param points: list of simple point coordinates [
            {"bID": int,
            "sIndex": int,
            "coords": [x, y]}
            , ...
        :return: None, fills up the self.nodes as a flat list
        """

        # Sorting the points based on their z-order score
        sortedPoints = sorted(points, key=lambda item: zOrder(*item["coords"]))

        # Splitting that sorted list into leaf node - chunks.
        # Each contains BLOCKSIZE//Entry-size entries
        for i in range(0, len(sortedPoints), self.nodeCap):
            leafNode = sortedPoints[i:i + self.nodeCap]
            self.nodes.append({"id": i // self.nodeCap,
                               "type": "l",
                               "level": 0,
                               "records": leafNode})  # FIXME: Update to include pointer to the data
            # Adding a bounding box attribute
            self.nodes[-1]["rectangle"] = RTReeUtil.leafBoundingRect([item["coords"] for item in self.nodes[-1]["records"]])



                                                    # Let's iterate through the leaf blocks to make parent nodes!
        buffer = []                                 # Buffer to temporarily encapsulate the node
        for i, leaf in enumerate(self.nodes):       # Adding items to that buffer until it fills

            buffer.append(leaf)
            if len(buffer) == self.nodeCap:         # Let's add to the end of the list a new block
                new_item = {"id" : len(self.nodes),
                            "children" : [child["id"] for child in buffer],
                            "level": buffer[0]["level"]+1,
                            "type": "n",
                            "rectangle" : RTReeUtil.rectBoundingBox([leafNode["rectangle"] for leafNode in buffer])}
                self.nodes.append(new_item)
                buffer = []





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
