from RTree import Rtree
import config
import pandas as pd
from copy import deepcopy
from matplotlib import pyplot as plt
import Queries



def plot(total, ours):
    
    clean_total = total[~total.apply(tuple,1).isin(ours.apply(tuple,1))]
    
    plt.scatter(clean_total['x'], clean_total['y'], color='blue', label='Total')
    plt.scatter(ours['x'], ours['y'], color='red', label='Query')
    
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot of Range Query')

    plt.legend()
    plt.show()
    
    


if __name__ == "__main__":
    tempTree = Rtree(config.INDEXFILE)
    
    
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
    
    
    
    query = Queries.rangeQuery(tempTree.nodes, tempTree.nodes["root"]["id"], [[414861000000, 264302000000], [415101000000, 264920000000]]) #261712831000
    
    query_df = pd.DataFrame(
        {
                "x": [leaf["coords"][0] for leaf in query],
                "y": [leaf["coords"][1] for leaf in query]
        }
    )
    
    plot(points, query_df)