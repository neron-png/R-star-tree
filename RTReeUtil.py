
###########
# Loading #
###########
def zOrder(*pointCoords, maxBitLen = None) -> int:
    """Computes the z-order index from coordinates in n dimensions

    :param (x, y, z ...): n-dimensional integer coordinates of point
    :param maxBitLen: None | Default, maximum size of outgoing z-number
    :return: number. the distance from (0, 0) to the point (x, y)
    """
    n = len(pointCoords)
    z = 0
    maxBitLen = max([coord.bit_length() for coord in pointCoords])*n
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
    """

    :param rectangles: [[[x, y,...n], [x', y',...n']], [[x1, y1,...n1], [x1', y1',...n1']]]
    :return: minimum bouding rectangle [[x, y,...n], [x', y',...n']]
    """
    rect = rectangles[0].copy()
    for rectangle in rectangles:
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


def rectangleContains(r: list, p: list) -> bool:
    for i in range(len(r[0])):
        if not ( p[i] >= r[0][i] and p[i] <= r[1][i] ):
            return False
        # print(f'{p[i]} >= {r[0][i]} and {p[i]} <= {r[1][i]}')
    return True