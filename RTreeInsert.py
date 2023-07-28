from Record import Record
from RTReeUtil import rectangleContains

def insert(nodeCap: int, nodes: dict, record: Record) -> dict:
    """
    :param Record dict: {
                        "bID": int,
                        "sID": int,
                        "coords": list [x, y, z...]
                        }
    :return: Nodes
    """
    
    point = record.coords    
    
    """ Choose subtree """
    def recursive_insert(pathOfIDs: list):
        
        item = nodes[pathOfIDs[-1]]
        
        if item["type"] == "l":            
            pass
        else:
            for childID in item["children"]:
                if rectangleContains(nodes[childID]["rectangle"], point):
                    pass
                    
                    
    recursive_insert([nodes["root"]["id"]])
    
    
    return nodes
