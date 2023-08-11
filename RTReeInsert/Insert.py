from pprint import pprint
from Record import Record
from RTReeUtil import rectangleContains, overlap, rectAddPoint, min_i, rectangleArea
import RTReeUtil
import config
from RTReeInsert.ChooseSubtree import chooseSubtreeLeaf, flatten, chooseSubtree
from RTReeInsert.FindSplit import findSplit
from random import randint


def insertData(nodeCap: int, m: int, nodes: dict, record: dict) -> dict: #TODO change record: List to record type object
    """
    :param Record dict: {
                        "name": str,
                        "coords": list [x, y, z...]
                        }
    :return: Nodes
    """

    """ 1. Insert the data to the datafile to retrieve the bID and sID """
    """ Create entry as such: {
                        "bID": int,
                        "sID": int,
                        "coords": list [x, y, z...]
                        }"""
    """ TODO the above """

    # FIXME remove
    entry = {"coords": record["coords"], "bID": 0, "sID": 0} 

    return insert(nodeCap=nodeCap, m=m, nodes=nodes, entry=entry, level=0)

    

def insert(nodeCap: int, m: int, nodes: dict, entry: dict, level: int) -> dict:
    """
    :return: Nodes
    """

    """ I1: Invoke chooseSubtree to find the subtree """
    if level == 0:
        subtree = chooseSubtreeLeaf(nodes, entry["coords"])
    else:
        subtree = chooseSubtree(nodes=nodes, level=level, rect=entry["rectanle"])
    subtree = flatten(subtree)

    pprint(findSplit(nodeCap=nodeCap, m=m, nodes=nodes, splitNodeID=subtree[-2]))
    """ I2: Accomodate Entry in N, check if overflown and call treatment """
    nodes[subtree[-1]].append(entry)
    if len(nodes[subtree[-1]]) >= nodeCap:
        overflowTreatment(nodes=nodes, nodeCap=nodeCap, level=level, m=m, overflownID=subtree[-1])

    """ I3: If overflow treatment was called and there was a split, propagate upwards """
    # TODO

    """ I4: Navigate the insertion path and recalculate the rectangles """
    # TODO

    return nodes


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def overflowTreatment(nodes: dict, nodeCap: int, level: int, m:int, overflownID: int):
    
    """ OT1: if level is not the root level and this is the first Overflow Treatment for this level """
    if config.OVERFLOWTREATMENT[level] == 0 and not nodes[nodes["root"]["id"]]["level"] == level:

        """ REINSERT """
        """ TODO """
        pass
    else:
        split_groups = findSplit(nodeCap=nodeCap, m=m, nodes=nodes, splitNodeID=overflownID)
        nodes[overflownID]["children"] = split_groups[0]

        max_existing_id = int(max(list(nodes.keys()))) #FIXME - ignore
        # nodes[max_existing_id+1] = {"id": max_existing_id+1, "level": level, "children": []}
        pass


def reinsert():
    pass