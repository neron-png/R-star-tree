import RTReeUtil as util

def rangeQuery(nodes:dict, nodeId: int, range: list) -> list:
    intersections = []
    result = []
    
    node = nodes[nodeId]

    if node["type"] == "n":
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
        for point in node["records"]:
            if util.rectangleContains(range, point["coords"]):
                result.append(point)
        return result
