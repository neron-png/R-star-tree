from RTreeNode import *
from Record import *
from storageHandler import *
from config import *


class RStarTree():

    def __init__(self):
        self.root = RTreeNode(block_id=0)
        self.currentBlock = self.root #This is a pointer!
        print(self.currentBlock)
        print(self.currentBlock.toBytes())


    def insert(self, record: Record, currentNode: RTreeNode = None):
        # * creating a leaf entry from the record
        leafEntry = RTreeEntry(data=record)

        # * Running the "choose subtree" algorithm until a leaf node is selected
        currentNode = self.root
        insertionNode = None

        while True:
            insertionNode = self._choose_subtree(record=record, currentNode=currentNode)
            if insertionNode.is_leaf_node:
                break

        # * Inserting into the chosen leaf node
        insertionNode.append(leafEntry)

        # * checking if oversized and splitting
        if insertionNode.isOversized():
            self._split_leaf(insertionNode)

    def _choose_subtree(self, record: Record, currentNode = None):

        # * Check if we can import it where we are (on the leaf)
        # Redundant code rn
        if currentNode.is_leaf_node:
            return currentNode

        # * Find a node to import it into
        else:
            sortedChildren = sorted([
                {
                    "expansion" : entry.calculateExpansion(record),
                    "entry": entry
                } for entry in currentNode
            ], key=lambda child: child["expansion"])

            # * Check if the block points to leaf nodes
            # * Almost linear split, non quadratic
            if currentNode[0].is_leaf_node:
                # ! [Minimum overlap cost]
                # ! Find entry in the current node which requires the least OVERLAP enlargement
                # ! in order to house the new record
                # ! Ties shall be resolved by classically (least area enlargement or least size in general)

                # ? [determine the nearly minimum overlap cost]
                # ? Sort in ascending order of necessary area enlargement
                # ? Find the minimum overlap cost within the first n rectangles (eg. 10?)

                sample = sortedChildren[:NODE_SAMPLE]

                minOverlap = None
                minOverlappingEntry = None

                for i, entry in enumerate(sample):
                    curr = entry["entry"]
                    overlap = 0

                    for j in range(i, len(sample)):
                        if i == j:
                            continue
                        other = sample[j][entry].rect
                        overlap += curr.rect.intersectSize(other)

                    if minOverlap == None or overlap < minOverlap:
                        minOverlap = overlap
                        minOverlappingEntry = curr


                N = RTreeNode().fromFileID(blockID=minOverlappingEntry.child_id)
                return N

            # * If the pointers do not point to leaf nodes
            else:
                # ! [Minimum area cost]
                # ! Classical pick, the one with the least area enlargement (not overlap)
                N = RTreeNode().fromFileID(blockID=sortedChildren[0]["entry"].child_id)
                return N

    #TODO
    def _split_leaf(self, node: RTreeNode):
        sorted_entries = sorted(node, key=lambda entry: entry.rect.get_min_coords())

        # currentNode[minEntry].recalculateRectangle(record)

        #
        # # Since the nodes below may split themselves, check after the recursion
        # if currentNode.isOversized():
        #     self._split_node(currentNode)


    #TODO
    def _split_node(self, node: RTreeNode):
        pass

    def search_record(self, p: Point) -> Record:
        """ Find a point indexed by the RTree """

        data_ref = self.find_path(self.root, p)[-1][-1]
        return fetchBlock(DATAFILE, data_ref[0])[data_ref[1]]


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
