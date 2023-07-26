import json
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

""" Which levels to display, None for all"""
displayLevels = (4, 5, 6)

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
    for item in contents:
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
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'bo')
    
    for i, rect in enumerate(rectangles):
        ax.add_patch( Rectangle(rect, rectangles_width[i][0], rectangles_width[i][1], fill=False, linewidth=rectangle_levels[i]+2, edgecolor=levelColors[rectangle_levels[i]]))
        if displayLabels:
            ax.text(rect[0], rect[1], rectangle_ids[i], fontsize=10+(rectangle_levels[i]+1))
    plt.show()
    
    
    # print(contents)        