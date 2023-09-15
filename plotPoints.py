import json
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

""" Which levels to display, None for all"""
displayLevels = (0,1)

displayLabels = True

levelColors = {
    0: "black",
    1: "lightseagreen",
    2: "lime",
    3: "gold",
    4: "red",
    5: "blue",
    6: "dodgerblue",
    7: "black",
    8: "black"
}


if __name__ == "__main__":
    
    contents = json.load(open("index.json", "r"))
    # with open("index.json", "r") as file:
    x = []
    y = []
    rectangles = []
    rectangles_width = []
    rectangle_ids = []
    rectangle_levels = []
    for item in list(contents.values()):
        try:
            if item["type"] == 'l':
                for point in item["records"]:
                    x.append(point["coords"][0])
                    y.append(point["coords"][1])
            if displayLevels == None or item["level"] in displayLevels:
                rectangles.append(tuple(item["rectangle"][0]))
                width = item["rectangle"][1][0] - item["rectangle"][0][0]
                height = item["rectangle"][1][1] - item["rectangle"][0][1]
                rectangles_width.append([width, height])
                rectangle_ids.append(item["id"])
                rectangle_levels.append(item["level"])
        except Exception as e:
            continue
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'bo')
    
    for i, rect in enumerate(rectangles):
        ax.add_patch( Rectangle(rect, rectangles_width[i][0], rectangles_width[i][1], fill=False, linewidth=rectangle_levels[i]+2, edgecolor=levelColors[rectangle_levels[i]]))
        if displayLabels:
            ax.text(rect[0], rect[1], rectangle_ids[i], fontsize=10+(rectangle_levels[i]+1))



    from RTree import Rtree
    import copy
    import config

    tempTree = Rtree(config.INDEXFILE)


    nodes = copy.deepcopy(tempTree.nodes)

    del nodes["root"]

    nodes = list(nodes.values())

    nodes = list( filter(lambda node: node["type"] == "l",  nodes) )

    leaf_points = []

    for leaf in nodes:
        leaf_points.extend(leaf["records"])

    import pandas as pd
    points = pd.DataFrame(
        {
                "x": [leaf["coords"][0] for leaf in leaf_points],
                "y": [leaf["coords"][1] for leaf in leaf_points]
        }
    )


    import Queries
    from TESTKnn import plot

    query = [o[0] for o in Queries.nearestNeighborsQuery(tempTree.nodes, tempTree.nodes[tempTree.nodes["root"]["id"]], [c * config.MANTISSA for c in [41.47, 26.16]], 55, [])]

    query_df = pd.DataFrame(
        {
                "x": [leaf["coords"][0] for leaf in query],
                "y": [leaf["coords"][1] for leaf in query]
        }
    )

    plot(points, query_df)



    
    
    # print(contents)        