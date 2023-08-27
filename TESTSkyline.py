from RTree import Rtree
import config
from paretoset import paretoset
import pandas as pd
from copy import deepcopy


""" 
pip install paretoset
pip install pandas
"""


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
    skyline_points = tempTree.skylineQuery()
    
    print(len(valid_skyline_points))
    print(len(skyline_points))
    
