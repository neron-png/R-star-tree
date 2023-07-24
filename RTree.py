import RTReeUtil
import config
from RTReeUtil import z_order
import json
from pprint import pprint  # FIXME debug



class Rtree():

    def __init__(self):
        self.nodeCap: int = config.BLOCKSIZE // config.ENTRYSIZE
        self.nodes = []
        # self.root = RTreeNode(block_id=0)
        # self.currentBlock = self.root  # This is a pointer!
        # print(self.currentBlock)
        # print(self.currentBlock.toBytes())


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
        # TODO: use the coordinates attribute once the schema is defined
        sortedPoints = sorted(points, key=lambda item: z_order(*item["coords"]))

        # Splitting that sorted list into leaf node - chunks.
        # Each contains BLOCKSIZE//Entry-size entries
        for i in range(0, len(sortedPoints), self.nodeCap):
            leafNode = sortedPoints[i:i + self.nodeCap]
            self.nodes.append({"id": i // self.nodeCap,
                               "bID": leafNode["bID"],
                               "sIndex": leafNode["sIndex"],
                               "type": "l",
                               "level": 0,
                               "coords": leafNode["coords"]})  # FIXME: Update to include pointer to the data
            # Adding a bounding box attribute
            self.nodes[-1]["rectangle"] = RTReeUtil.leaf_bounding_rect(self.nodes[-1]["coords"])

        # FIXME
        # pprint(self.nodes[-10:])
        # pprint(self.nodes[:4])
        # print([x["rectangle"] for x in self.nodes[:4]])
        # print(RTReeUtil.rect_bounding_box([x["rectangle"] for x in self.nodes[:4]]))
        # FIXME

                                                    # Let's iterate through the leaf blocks to make parent nodes!
        buffer = []                                 # Buffer to temporarily encapsulate the node
        for i, leaf in enumerate(self.nodes):       # Adding items to that buffer until it fills

            # if leaf["type"] == "n":
            #     break

            buffer.append(leaf)
            if len(buffer) == self.nodeCap:         # Let's add to the end of the list a new block
                new_item = {"id" : len(self.nodes),
                            "children" : [child["id"] for child in buffer],
                            "level": buffer[0]["level"]+1,
                            "type": "n",
                            "rectangle" : RTReeUtil.rect_bounding_box([leafNode["rectangle"] for leafNode in buffer])}
                self.nodes.append(new_item)
                buffer = []

        # FIXME
        pprint(self.nodes)
        nestedlist = RTReeUtil.toNestedJson(self.nodes)
        print(json.dumps(nestedlist))
        # FIXME


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
        for i, item in enumerate(block): 
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
