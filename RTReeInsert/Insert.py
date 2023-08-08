from Record import Record
from RTReeUtil import rectangleContains, overlap, rectAddPoint, min_i, rectangleArea
import RTReeUtil
import config
from RTReeInsert.ChooseSubtree import chooseSubtree, flatten
from RTReeInsert.FindSplit import findSplit


# def insert(nodeCap: int, nodes: dict, record: Record) -> dict:
def insert(nodeCap: int, m: int, nodes: dict, record: list) -> dict:
    """
    :param Record dict: {
                        "bID": int,
                        "sID": int,
                        "coords": list [x, y, z...]
                        }
    :return: Nodes
    """
    
    point = record #TODO update
    subtree = chooseSubtree(nodes, point)
    subtree = flatten(subtree)
    # print(subtree)

    """ insert(subtree[-1]) """
    """ if subtree[-1] overflown, overflow treatment """
    """     if split, doing the split algorithm """

    split = findSplit(nodeCap=nodeCap, m=m, nodes=nodes, splitNodeID=subtree[-1])
    print(split)
    return nodes
