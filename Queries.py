import RTReeUtil as util
from RTree import Rtree

def rangeQuery(rtree: Rtree, rootNode: dict, range: list) -> list:
    intersections = []
    result = []
    
    if rootNode["type"] == "n":
        if util.rectangleIntersection(rootNode["rectangle"], range):
            for child in rootNode["children"]:
                if util.rectangleIntersection(rtree.nodes[child]["rectangle"], range):
                    intersections.append(child)

            for i in intersections:
                result.extend(rangeQuery(rtree, rtree.nodes[i], range))
            
            return result 
        else:
            return []
    else:
        for point in rootNode["records"]:
            if util.rectangleContains(range, point["coords"]):
                result.append(point)
        return result
