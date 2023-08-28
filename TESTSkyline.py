from RTree import Rtree
import config
from paretoset import paretoset
import pandas as pd
from copy import deepcopy
from matplotlib import pyplot as plt
import Queries

""" 
pip install paretoset
pip install pandas
"""


def plot(their, ours, total):
    
    clean_total = total[~total.apply(tuple,1).isin(their.apply(tuple,1))]
    
    plt.scatter(clean_total['x'], clean_total['y'], color='blue', label='Total')
    plt.scatter(their['x'], their['y'], color='red', label='Pareto')
    
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot of Library')

    plt.legend()
    plt.show()
    
    new_ours = pd.DataFrame(
        {
                "x": [leaf["coords"][0] for leaf in ours],
                "y": [leaf["coords"][1] for leaf in ours]
        }
    )
    
    clean_total = total[~total.apply(tuple,1).isin(new_ours.apply(tuple,1))]
    
    plt.scatter(clean_total['x'], clean_total['y'], color='blue', label='Total')
    plt.scatter(new_ours['x'], new_ours['y'], color='red', label='Pareto')
    
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot of Ours')

    plt.legend()
    plt.show()


if __name__ == "__main__":
    
    # StorageHandler.write_blocks_to_datafile()
    # tempTree = Rtree()
    tempTree = Rtree(config.INDEXFILE)
    # parseData = RTReeUtil.parseDataJson()
    # tempTree.bottom_up(parseData)
    
    nodes = deepcopy(tempTree.nodes)
    
    del nodes["root"]
    
    nodes = list(nodes.values())
    
    nodes = list( filter(lambda node: node["type"] == "l",  nodes) )
    
    leaf_points = []
    
    for leaf in nodes:
        leaf_points.extend(leaf["records"])
    
    
    points = pd.DataFrame(
        {
                "x": [leaf["coords"][0] for leaf in leaf_points],
                "y": [leaf["coords"][1] for leaf in leaf_points]
        }
    )
    
    
    # print(tempTree.skylineQuery())
    mask = paretoset(points, sense=["min", "min"])
    
    valid_skyline_points = points[mask]
    
    # skyline_points = tempTree.skylineQuery()
    skyline_points = Queries.skylineQuery(tempTree.nodes)
    plot(valid_skyline_points, skyline_points, points)
    
    print(len(valid_skyline_points))
    print(len(skyline_points))
    
