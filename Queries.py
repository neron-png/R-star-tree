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


def skylineQuery(nodes: dict) -> list:
    """
    The algorithm keeps the discovered skyline points in the set S.
    If the top of the queue is a data point, it is tested if it is dominated by any point in S.
    If yes, it is rejected, otherwise it is inserted into S
    """

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

    return S


def nearestNeighborsQuery(nodes: dict, currentNode, queryPoint, k: int, bestNeighbors: list):
    if currentNode["type"] == "l":
        for point in currentNode["records"]:
            distance = util.euclideanDistance(queryPoint, point["coords"])
            bestNeighbors.append((point, distance))
        bestNeighbors.sort(key=lambda x: x[1])
        return bestNeighbors[:k]

    # Sort child nodes by distance to query point
    currentNode["children"].sort(key=lambda child: util.calculateMinDistance(nodes[child]["rectangle"], queryPoint))

    for childId in currentNode["children"]:
        if len(bestNeighbors) > 0 and not util.calculateMinDistance(nodes[childId]["rectangle"], queryPoint) < bestNeighbors[-1][1]:
            break  # Skip this child, it cannot contain closer points
        bestNeighbors = nearestNeighborsQuery(nodes, nodes[childId], queryPoint, k, bestNeighbors)
        bestNeighbors.sort(key=lambda x: x[1])
        bestNeighbors = bestNeighbors[:k]

    return bestNeighbors


