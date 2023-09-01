import RTReeUtil
import config
from RTReeUtil import zOrder
import math

def bottom_up(nodeCap: int, nodes: dict, points) -> dict:
        """
        :param points: list of simple point coordinates 
            [{"bID": int,
            "sIndex": int,
            "coords": [x, y]}
            , ...
        :return: None, fills up the nodes as a flat list
        """
        if nodes["root"]["first_insert"]:
            nodes["root"]["first_insert"] = False
        # Sorting the points based on their z-order score
        sortedPoints = sorted(points, key=lambda item: zOrder(*item["coords"]))

        # Splitting that sorted list into leaf node - chunks.
        # Each contains BLOCKSIZE//Entry-size entries
        for i in range(0, len(sortedPoints), nodeCap):
            leafRecords = sortedPoints[i:i + nodeCap]
            id = i // nodeCap
            nodes[id] = {      "id": i // nodeCap,
                                "type": "l",
                                "level": 0,
                                "records": leafRecords,
                                "rectangle": RTReeUtil.leafBoundingRect([item["coords"] for item in leafRecords])}
            # Adding a bounding box attribute

        """
        # while sortedPoints:
        #     leafRecords = sortedPoints[0:nodeCap]
        #     nodes.append({      "id": len(nodes),
        #                         "type": "l",
        #                         "level": 0,
        #                         "records": leafRecords})
        #     # Adding a bounding box attribute
        #     nodes[-1]["rectangle"] = RTReeUtil.leafBoundingRect([item["coords"] for item in leafRecords])
        #     del sortedPoints[0:len(leafRecords)]
        """

        
        n = len(nodes)
        expansion_ration = nodeCap
        expected_max_height = math.ceil(math.log( n*(expansion_ration-1)+1 ,expansion_ration)) + 1
        
        
        for level in range(expected_max_height):
            levelCount = 0
            buffer = []                                 # Buffer to temporarily encapsulate the node
            for nodeID in list(nodes):                        # Adding items to that buffer until it fills
                if nodeID == "root":
                    continue
                
                node = nodes[nodeID]
                if node["level"] == level:
                    
                    buffer.append(node)
                    if len(buffer) == nodeCap:         # Let's add to the end of the list a new block
                        id = len(nodes)
                        new_item = {"id" : id,
                                    "children" : [child["id"] for child in buffer],
                                    "level": level+1,
                                    "type": "n",
                                    "rectangle" : RTReeUtil.rectBoundingBox([bufferNode["rectangle"] for bufferNode in buffer])}
                        
                        nodes[id] = new_item
                        buffer = []
                        levelCount += 1
            else:                                       # Check for residuals
                if (buffer and levelCount > 0) or (levelCount == 0 and len(buffer) > 1):
                    id = len(nodes)
                    new_item = {"id" : id,
                                    "children" : [child["id"] for child in buffer],
                                    "level": level+1,
                                    "type": "n",
                                    "rectangle" : RTReeUtil.rectBoundingBox([bufferNode["rectangle"] for bufferNode in buffer])}
                    nodes[id] = new_item
                    buffer = []
            level += 1
        
        
        nodes["root"]["id"], nodes["root"]["level"] = RTReeUtil.findRoot(nodes)

        return nodes