import math
import config

###########
# Loading #
###########

def inRectangle(point: list, rectangle: list):
    """
    
    :param  point -> (x, y, z ...): n-dimensional integer coordinates of point
            rectangle -> [(x1, y1, z1 ...), (x2, y2, z2 ...)]
    :return: bool. the distance from (0, 0) to the point (x, y)
    """
    
    for i, coord in enumerate(point):
        if not coord >= rectangle[0][i] or not coord <= rectangle[1][i]:
            return False
                
    
    return True


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
                                "sIndex": item["id"],
                                "coords": item["coords"]
                            }
            parsedSample.append( parsedItem )

    return parsedSample




def zOrder(*pointCoords, maxBitLen = None) -> int:
    """Computes the z-order index from coordinates in n dimensions

    :param (x, y, z ...): n-dimensional integer coordinates of point
    :param maxBitLen: None | Default, maximum size of outgoing z-number
    :return: number. the distance from (0, 0) to the point (x, y)
    """
    n = len(pointCoords)
    z = 0
    maxBitLen = int(max([coord.bit_length() for coord in pointCoords]))*n
    # maxBitLen = sum([coord.bit_length() for coord in pointCoords])

    for i in range(0, maxBitLen // n):
        for j in range(n):
            # Shifting each dimension coordinate `i` places and then giving it an offset
            z += ((pointCoords[j] >> i) & 1) << ((i * n) + j)

    return z


def leafBoundingRect(leaf_coordinates):
    """

    :param leaf_coordinates: - schema:   [[416101905000, 265951733000],
                                         [413692356000, 266291197000],
                                         [413692356000, 266297380000],
                                         [413691693000, 266302826000]]
    :return: [[x, y,...n], [x', y',...n']]
    """

    low_corner = leaf_coordinates[0].copy()
    high_corner = leaf_coordinates[0].copy()
    for item in leaf_coordinates:
        for i, coordinate in enumerate(item):
            if coordinate < low_corner[i]:
                low_corner[i] = coordinate
            if coordinate > high_corner[i]:
                high_corner[i] = coordinate

    return [low_corner, high_corner]

def rectBoundingBox(rectangles):
    import copy
    """

    :param rectangles: [[[x, y,...n], [x', y',...n']], [[x1, y1,...n1], [x1', y1',...n1']]]
    :return: minimum bouding rectangle [[x, y,...n], [x', y',...n']]
    """
    newRectangles = copy.deepcopy(rectangles)
    rect = newRectangles[0]
    for rectangle in newRectangles:
        for i in range(2):
            for j, coordinate in enumerate(rectangle[i]):
                if i == 0:
                    if coordinate < rect[0][j]:
                        rect[0][j] = coordinate
                else:
                    if coordinate > rect[1][j]:
                        rect[1][j] = coordinate
    return rect


def toNestedJson(nodeList: list):
    newArray = {}
    seenKeys = set()

    def traverse(id):
        item = nodeList[id]
        seenKeys.add(id)
        if "children" not in item.keys():
            return str(item["id"])
            # return str(item)
        else:
            return {str(id): [traverse(childID) for childID in item["children"]]}

    for item in reversed(nodeList):
        if item["id"] not in seenKeys:
            newArray[item["id"]] = traverse(item["id"])

    return newArray


def rectangleIntersection(r1: list, r2: list) -> bool:
    for i, c in enumerate(r1[0]):
        if not r2[1][i] >= c:
            return False

    for i, c in enumerate(r1[1]):
        if not r2[0][i] <= c:
            return False
    
    return True


def rectangleContains(rectangle: list, point: list) -> bool:
    """_summary_

    Args:
        rectangle (list): [[x1, y1, z1...], [x2, y2, z2...]]
        point (list): [x, y, z...]

    Returns:
        bool: is the point in the rectangle?
    """
    for i in range(len(rectangle[0])):
        if not ( point[i] >= rectangle[0][i] and point[i] <= rectangle[1][i] ):
            return False
        # print(f'{p[i]} >= {r[0][i]} and {p[i]} <= {r[1][i]}')
    return True


###########
# General #
###########

def min_i(iterable: list):
    min_i = 0
    min_e = iterable[0]
    
    for i, e in enumerate(iterable):
        if e < min_e:
            min_e = e
            min_i = i
    
    return min_e, min_i


def findRoot(nodes: dict) -> tuple:
    maxlvl = 0
    maxID = 0

    for nodeID in list(nodes):
        if nodes[nodeID]["level"] > maxlvl:
            maxID = nodeID
            maxlvl = nodes[nodeID]["level"]
    
    return maxID, maxlvl


def intObjectHook(x):
    return {int(k) if k.lstrip('-').isdigit() else k: v for k, v in x.items()}

"""

def rectBoundingBox(rectangles: list):
    \"\"\"_summary_

    Args:
        rectangles (list): list of rectangles [ [[x1, y1, z1...], [x2, y2, z2...]], [[xb, yb, zb...], [xb, yb, zb...]] ]
    \"\"\"
    dimensions = len(rectangles[0][0])
    
    near_corner = [min([rectangle[0][i] for rectangle in rectangles]) for i in range(dimensions)]
    far_corner = [max([rectangle[1][i] for rectangle in rectangles]) for i in range(dimensions)]
    return [near_corner, far_corner]
"""

def rectIntersection(rectangles: list) -> list:
    """_summary_

    Args:
        rectangles (list): list of rectangles [ [[x1, y1, z1...], [x2, y2, z2...]], [[xb, yb, zb...], [xb, yb, zb...]] ]

    Returns:
        Intersection of all the rectangles: [[x1, y2, zk], [x5, yk, z2]]
    """
    
    if len(rectangles) < 2:
        return rectangles[0]
    intersection = rectangles[0]
    
    dimensions = len(intersection[0])
    for rect in rectangles[1:]:
        new_intersection = [[] for __ in range(2)]
        
        for dimension in range(dimensions):
            min_val = max(intersection[0][dimension], rect[0][dimension])
            max_val = min(intersection[1][dimension], rect[1][dimension])
            if min_val > max_val:
                return [None]  # No intersection
            new_intersection[0].append(min_val)
            new_intersection[1].append(max_val)
        intersection = new_intersection

    return intersection


def rectAddPoint(rectangle: list, point: list):
    """_summary_

    Args:
        rectangle (list): [[x1, y1, z1...], [x2, y2, z2...]]
        point (list): [x, y, z...]

    Returns:
        _type_: _description_
    """
    return rectBoundingBox(rectangles=[rectangle, [point, point]])

def rectangleArea(rectangle: list):
    """_summary_

    Args:
        rectangle (list): [[x1, y1, z1...], [x2, y2, z2...]]
    returns: Area: int
    """
    return math.prod( [rectangle[1][dimension] - rectangle[0][dimension] 
                    for dimension in range(len(rectangle[0]))])


def overlap(rectangle: list, nodeRectangles:list):
    """_summary_

    Args:
        rectangle (list): [[x1, y1, z1...], [x2, y2, z2...]]
        nodeRectangles (list): list of rectangles
    """
    myArea = rectangleArea(rectangle) # Need to exclude the rectangle's own area
    areaSum = 0
    for otherRectangle in nodeRectangles:
        otherIntersect = rectIntersection([rectangle, otherRectangle])
        if otherIntersect[0] is None:
            continue
        otherArea = rectangleArea(otherIntersect)
        areaSum += otherArea
    
    return areaSum - myArea

##########
# INSERT #
##########

def margin(rectangle: list) -> int:
    """ Sum of the lengths of the edges of a rectangle
        aka Perimeter :()

        parameter: rectangle = [[x1, y1, z1...], [x2, y2, z2...]]
    """

    margin = 0
    for axis in range(len(rectangle[0])):
        margin += rectangle[1][axis] - rectangle[0][axis]
    
    return margin


class MinHeapElement:
    def __init__(self, node: dict):
        self.node = node
        if node["type"] == "n":
            self.type = "rectangle"
            self.l1 = sum(node["rectangle"][0])
        else:
            self.type = "point"
            self.l1 = sum(node["coords"])

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, node):
        item = MinHeapElement(node)
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent_idx = (index - 1) // 2
        while index > 0 and self.heap[index].l1 < self.heap[parent_idx].l1:
            self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
            index = parent_idx
            parent_idx = (index - 1) // 2

    def _heapify_down(self, index):
        left_child_idx = 2 * index + 1
        right_child_idx = 2 * index + 2
        smallest = index

        if left_child_idx < len(self.heap) and self.heap[left_child_idx].l1 < self.heap[smallest].l1:
            smallest = left_child_idx
        if right_child_idx < len(self.heap) and self.heap[right_child_idx].l1 < self.heap[smallest].l1:
            smallest = right_child_idx

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
