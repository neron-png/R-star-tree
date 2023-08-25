import StorageHandler

def delete(nodes, nodeCap, id):
    """
    @params: Node id, id of node to be deleted
        @return: (True) if found and deleted | (False, "Reason") if not succeeded
    """
    
    christosHasFixedIt = True
    if christosHasFixedIt:
        exists, item = StorageHandler.searchByID(id)
        print(exists, item)
        if not exists:
            return (False, item)

    #TODO update block on disk

    #TODO update RTree with reinsert and that shit

