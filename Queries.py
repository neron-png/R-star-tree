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


# def skylineQuery(nodes: dict) -> list:
#     """
#     The algorithm keeps the discovered skyline points in the set S.
#     If the top of the queue is a data point, it is tested if it is dominated by any point in S.
#     If yes, it is rejected, otherwise it is inserted into S
#     """

#     root = nodes[nodes["root"]["id"]]

#     S = []
#     # S contains records, i.e.: {"bID": 1011, "sIndex": 1861645905, "coords": [414867382000, 261587580000]}
#     # heap initilized with root, i.e.:
#     # {"id": 2784, "children": [2781, 2782, 2783, 2790], "level": 6, "type": "n", "rectangle": [[413672855000, 261587580000], [416101905000, 266318299000]]}

#     heap = util.MinHeap()
#     heap.push(root)

#     while heap.heap:
#         top = heap.pop()

#         if top is not None and nodes[top.id]["type"] == "n":
#             flag = True
#             for point in S:
#                 if util.isDominated(nodes[top.id]["rectangle"][0], point["coords"]):
#                     flag = False
#                     break
#             if flag:
#                 for childId in nodes[top.id]["children"]:
#                     heap.push(nodes[childId])

#         elif top is not None and nodes[top.id]["type"] == "l":
#             for child in nodes[top.id]["records"]:
#                 flag = True
#                 for point in S:
#                     if util.isDominated(child["coords"], point["coords"]):
#                         flag = False
#                         break
#                 if flag:
#                     S.append(child)

#     return S


def skylineQuery(nodes: dict) -> list:
    root = nodes[nodes["root"]["id"]]
    S = []

    import heapq

    minHeap = []

    heapq.heappush(minHeap, (sum(root["rectangle"][0]), root["id"]))

    while minHeap:
        top = heapq.heappop(minHeap)

        if nodes[top[1]]["type"] == "n":
            flag = True
            for point in S:
                if util.isDominated(nodes[top[1]]["rectangle"][0], point["coords"]):
                    flag = False
                    break
            if flag:
                for childId in nodes[top[1]]["children"]:
                    heapq.heappush(minHeap, (sum(nodes[childId]["rectangle"][0]), nodes[childId]["id"]))
        else:
            dominants = []
            flag = True

            for child in nodes[top[1]]["records"]:
                for other in nodes[top[1]]["records"]:
                    if util.isDominated(child["coords"], other["coords"]):
                        flag = False
                        break

                if flag:
                    dominants.append(child)

            flag = True

            for dominant in dominants:
                for point in S:
                    if util.isDominated(dominant["coords"], point["coords"]):
                        flag = False
                        break
                if flag:
                    S.append(dominant)

    print(S)
    return S
