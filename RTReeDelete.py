import StorageHandler
from RTReeInsert.ChooseSubtree import chooseSubtreeLeaf, flatten
from copy import deepcopy
import RTReeUtil

def delete(nodes, nodeCap, m, id):
    """
    @params: Node id, id of node to be deleted
        @return: (True) if found and deleted | (False, "Reason") if not succeeded
    """
    
    
    exists, item, bID = StorageHandler.searchByID(id)
    
    if not exists or not item or not bID:
        return (False, item)

    StorageHandler.deleteRecordFromDisk(bId=bID, sId=id)
    
    subtree = flatten(chooseSubtreeLeaf(nodes=nodes, point=item["coords"]))
    subtree.reverse()
    
    
    reinsertions = []
    leafID = subtree[0]
    underflowFlag = False
    
    """ Deleting the record from the list """
    nodes[leafID]["records"] = list( filter(lambda record: record["sIndex"] != id,  nodes[leafID]["records"]) )
    
    
    """ Checking for underfill """
    if len(nodes[leafID]["records"]) < m:
        """ Saving records for reinsert """
        for record in nodes[leafID]["records"]:
            reinsertions.append( (deepcopy(record), nodes[leafID]["level"]) )
        underflowFlag = True
        del nodes[leafID]
    else:
        """ Adjusting rectangles """
        nodes[leafID]["rectangle"] = RTReeUtil.leafBoundingRect([record["coords"] for record in nodes[leafID]["records"]])
        for upperID in subtree[1:]:
            nodes[upperID]["rectangle"] = RTReeUtil.rectBoundingBox([nodes[ID]["rectangle"] for ID in nodes[upperID]["children"]])
        return (True, item)
    
    """ If the leaf node was underflown and deleted, we have to propagate changes upwards """
    # print(subtree)
    for i, ID in enumerate(subtree[1:]):
        if underflowFlag:
            # print(ID)
            # print(nodes[ID])
            # print(subtree[i-1])
            nodes[ID]["children"].remove(subtree[i])
            
            if len(nodes[ID]["children"]) < m:
                for nodeID in nodes[ID]["children"]:
                    reinsertions.append( (deepcopy(nodes[nodeID]), nodes[nodeID]["level"]) )
                    del nodes[nodeID]
            else:
                underflowFlag = False
                for upperID in subtree[i+1:]:
                    nodes[upperID]["rectangle"] = RTReeUtil.rectBoundingBox([nodes[ID]["rectangle"] for ID in nodes[upperID]["children"]])
                break
    
    import RTReeInsert.Insert
    for reinsertion in reinsertions:
        RTReeInsert.Insert.insert(m=m, nodes=nodes, nodeCap=nodeCap, level=reinsertion[1], entry=reinsertion[0])
    