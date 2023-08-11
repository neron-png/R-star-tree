from pprint import pprint
from Record import Record
from RTReeUtil import rectIntersection, rectangleArea, rectangleContains, overlap, rectAddPoint, min_i, margin, rectBoundingBox
import RTReeUtil
import config


def findSplit(nodeCap: int, m: int, nodes: dict, splitNodeID: int):
    import copy
    """ S1: Choose Split Axis """
    """ S2: Choose Split Index """
    """ S3: Distribute into two groups"""

    nodes = copy.deepcopy(nodes)
    node = copy.deepcopy(nodes[splitNodeID])

    """ If it's a leaf node, let's do a bit of a hack to make it compatible :/ """
    """ I am tired """
    
    if node["type"] == "n":
        originalChildrenEntries = [nodes[childID] for childID in node["children"]]
    else:
        
        node["children"] = node["records"]
        for i, record in enumerate(node["children"]):
            node["children"][i]["rectangle"] = [node["children"][i]["coords"], node["children"][i]["coords"]]
        
        originalChildrenEntries = node["children"]

    childrenEntries = originalChildrenEntries.copy()


    """ S1 """
    """ Choose Split Axis """

    """ For each axis """
    axisSums = {}
    for axis in range(len(node["rectangle"][0])):
        axisSums[axis] = 0

        """ Sort each entry by the lower, then upper corner of the rectangle """
        for i in range(2):
            childrenEntries.sort(key= lambda entry: entry["rectangle"][i][axis])

            """ For each distribution determine it's S value (margin)"""
            for k in range(1, nodeCap - 2*m + 2):
                slit = (m-1)+k
                groupA = copy.deepcopy(childrenEntries[:slit])
                
                groupB = copy.deepcopy(childrenEntries[slit:])
                # print("..............")
                # print([child["rectangle"] for child in groupA])
                bbA = rectBoundingBox([child["rectangle"] for child in groupA])
                # print([child["rectangle"] for child in groupB])
                bbB = rectBoundingBox([child["rectangle"] for child in groupB])

                """ Sum the S values """
                axisSums[axis] += margin(bbA) + margin(bbB)
    
    minAxis = min(axisSums.keys(), key=lambda axis: axisSums[axis])

    """ S2 """
    """ Choose Split Index """

    childrenEntries.sort(key= lambda entry: entry["rectangle"][0][minAxis]) #TODO this seems iffy
    overlapValue = {}
    for k in range(1, nodeCap - 2*m + 2):
        slit = (m-1)+k

        groupA = copy.deepcopy(childrenEntries[:slit])
        groupB = copy.deepcopy(childrenEntries[slit:])

        # print("..............")
        # print([child["rectangle"] for child in groupA])
        bbA = rectBoundingBox([child["rectangle"] for child in groupA])
        # print([child["rectangle"] for child in groupB])
        bbB = rectBoundingBox([child["rectangle"] for child in groupB])

        """ Sum the S values """
        intersection = rectIntersection([bbA, bbB])
        if not intersection[0] is None:
            overlapValue[slit] = rectangleArea(intersection)
        else:
            overlapValue[slit] = 0
        
    splitIndex = min(list(overlapValue.items()), key=lambda item: item[1])[0]

    return [item["id"] for item in childrenEntries[:splitIndex]], [item["id"] for item in childrenEntries[splitIndex:]]


    