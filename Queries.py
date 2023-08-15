import RTReeUtil as util

def rangeQuery(nodes:dict, nodeId: int, range: list) -> list:
    """
    :param nodes: dict of all r-tree nodes
    :param nodeId: examinating node id 
    :param range: list of (n-1)-d rectangle's corners
    :return: list of node elements included in the range
    """

    intersections = []
    result = []
    
    # Get the root/parent node
    node = nodes[nodeId]

    if node["type"] == "n":
        
        # if node is not a leaf (so, does not contains points)
        # check if intersects with the given area (range) and take its content
        # (rectangles) to check their intersection (recursivly)

        if util.rectangleIntersection(node["rectangle"], range):
            for child in node["children"]:
                if util.rectangleIntersection(nodes[child]["rectangle"], range):
                    intersections.append(child)

            for i in intersections:
                result.extend(rangeQuery(nodes, i, range))
            
            return result 
        else:
            return []
    else:

        # if the node is a leaf, return the elements (points) contained in the range

        for point in node["records"]:
            if util.rectangleContains(range, point["coords"]):
                result.append(point)
        return result


def skylineQuery(nodes: dict):
    pass