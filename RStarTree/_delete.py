from RTreeNode import *
from Record import *
from storageHandler import *
from config import *

def delete_entry(self, p: Point):
    """ Delete an index record with given coordinates """

    # Find the path from root to leaf RTreeNode that contains the given point
    path = self.find_path(self, self.root, p)

    # Remove the RTreeEntry indexing point p
    self.delete_from_node(path[-1], p)

    # Condense the affected path of RTreeNodes
    self.condense_path(path)


def condense_path(self, path: tuple):
    """ Condense a list of hierarchically connected RTreeNodes """

    for i in range(len(path) - 1, -1, -1):
        node_id, slot_id, entry_data = path[i]

        node = fetchBlock(INDEXFILE, node_id)

        # TODO: the following

        if len(node) < NODE_MIN_ENTRIES:
            self.adjust_node(node)
        # if i > 0:
        #     parent, parent_entry = path[i - 1]
        #
        #     if len(node.entries) == 0:
        #         parent.entries.remove(parent_entry)
        #     else:
        #         parent_entry.rect = calculate_enclosing_rect(node.entries)


def redistribute_entries(self, node: RTreeNode):
    pass


def reinsert_entries(self, node: RTreeNode):
    pass


def adjust_node(self, node: RTreeNode):
    if node.is_leaf_node:
        self.redistribute_entries(node)
    else:
        self.reinsert_entries(node)
    pass


def delete_from_node(self, dest_details: tuple, p: Point):
    """ Delete the RTreeEntry, indexing point p, from an RTreeNode """

    # Fetch the RTreeEntry indexing point p
    node = fetchBlock(INDEXFILE, dest_details[0])

    # Remove the RTreeEntry from the node
    node.pop(dest_details[1])

    # Store the updated RTreeNode back to disk
    storeBlock(node)

    # TODO: delete record from DATAFILE (block-id, slot-id = node[2][0], node[1][1])


def find_path(self, node: RTreeNode, p: Point) -> list:
    """ Keep track of the block-and-slot ids of the RTreeNodes/Entries that
        lead to the wanted leaf
    """

    # Fetch the search subtree root RTreeNode
    fetched_node = fetchBlock(INDEXFILE, node.block_id)

    # If RStarTree's root node is a leaf
    if fetched_node.is_leaf_node:
        for entry in fetched_node:
            if entry.rect.contains_point(p):
                return [(fetched_node.block_id, 0, entry.data)]

    # Else there are more than one levels in the RStarTree
    # Initialize block-and-slot-ids path
    path = []

    while not fetched_node.is_leaf_node:
        for slot_id, entry in enumerate(fetched_node):
            if entry.rect.contains_point(p):
                path.append((fetched_node.block_id, slot_id, entry.data))
                if not entry.is_leaf_entry:
                    fetched_node = fetchBlock(INDEXFILE, entry.child_id)
                    break
                else:
                    return path
    return path