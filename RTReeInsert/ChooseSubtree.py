from Record import Record
from RTReeUtil import rectangleContains, overlap, rectAddPoint, min_i, rectangleArea
import RTReeUtil
import config


def flatten(subtree) -> list:
    """
    input: subtree: [2784, [2781, [2772, [2739, [2608, [2086, 0]]]]]]
    returns: subtree: [2784, 2781, 2772, 2739, 2608, 2086, 0]
    """
    if not isinstance(subtree[1], list):
        return subtree
    else:
        newtree = [subtree[0]]
        newtree.extend(flatten(subtree[1]))
        return newtree
    


def chooseSubtree(nodes: dict, point: list) -> list:
    
    """ Choose subtree """
    def recursiveChoose(N_ID):
        
        currentNode = nodes[N_ID]
        
        """ CS2 """
        # IF
        if currentNode["type"] == "l":
            return currentNode["id"]
        
        # ELSE
        else:
            # IF this ID points to leaves, calculating overlap
            if nodes[currentNode["children"][0]]["type"] == "l":
                
                """ Reducing the overlap cost by sorting by area enlargement """
                childrenNodes = [nodes[id] for id in currentNode["children"]]
                childrenNodes.sort(key= lambda node: rectangleArea(rectAddPoint(node["rectangle"], point)) - rectangleArea(node["rectangle"]))
                childrenIDs = [child["id"] for child in childrenNodes[:config.P]]
                
                # Picking the child ID with the least overlap enlargement
                childrenRectangles = [nodes[childID]["rectangle"] for childID in childrenIDs]
                childrenOverlapEnlargements = []
                for i, id in enumerate(childrenIDs):
                    # Calculating initial overlap
                    initialRectangle = childrenRectangles[i]
                    initialOverlap = overlap(initialRectangle, childrenRectangles)

                    # Calculating overlap after adding the point
                    newRect = rectAddPoint(initialRectangle, point)
                    newChildrenRectnangles = childrenRectangles[:i] + [newRect] + childrenRectangles[i+1:]
                    newOverlap = overlap(newRect, newChildrenRectnangles)
                    childrenOverlapEnlargements.append(newOverlap - initialOverlap)
                
                minimumChildRectangleIndex = min_i(childrenOverlapEnlargements)[1]
                return [N_ID, recursiveChoose(childrenIDs[minimumChildRectangleIndex])]
                
            # ELSE this ID points to nodes, calculating enlargement
            else:
                childrenIDs = currentNode["children"]
                childrenRectangles = [nodes[childID]["rectangle"] for childID in childrenIDs]
                childrenAreaEnlargements = []
                
                for i, id in enumerate(childrenIDs):
                    # Calculating initial areas
                    oldArea = rectangleArea(childrenRectangles[i])
                    newArea = rectangleArea(rectAddPoint(childrenRectangles[i], point))
                    childrenAreaEnlargements.append(newArea - oldArea)
                
                minimumChildRectangleIndex = min_i(childrenAreaEnlargements)[1]
                return [N_ID, recursiveChoose(childrenIDs[minimumChildRectangleIndex])]
                
    """ CS1 """    
    return recursiveChoose(nodes["root"]["id"])