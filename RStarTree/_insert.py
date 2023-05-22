from Record import *
from RTreeNode import *
from config import *


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


def _choose_subtree(self, record: Record, currentNode=None):
    # * Check if we can import it where we are (on the leaf)
    # Redundant code rn
    if currentNode.is_leaf_node:
        return currentNode

    # * Find a node to import it into
    else:
        sortedChildren = sorted([
            {
                "expansion": entry.calculateExpansion(record),
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


# TODO
def _split_leaf(self, node: RTreeNode):
    sorted_entries = sorted(node, key=lambda entry: entry.rect.get_min_coords())

    # currentNode[minEntry].recalculateRectangle(record)

    #
    # # Since the nodes below may split themselves, check after the recursion
    # if currentNode.isOversized():
    #     self._split_node(currentNode)


# TODO
def _split_node(self, node: RTreeNode):
    pass


def _choose_split_axis(self, node: RTreeNode) -> int:
    axis_count = len(node[0].rect.get_min_coords())
    distributionCount = node.M() - 2 * node.m() + 2
    minAxis = None
    minMetric = None

    for axis in range(axis_count):
        metric = 0

        for corner in ("min", "max"):
            if corner == "min":
                grouping = sorted(node, key=lambda entry: entry.rect.get_min_coords()[axis])
            else:
                grouping = sorted(node, key=lambda entry: entry.rect.get_max_coords()[axis])

            for k in range(1, distributionCount):
                group1 = grouping[:(node.m() - 1) + k]
                group2 = grouping[(node.m() - 1) + k:]

                margin_bb1 = Rectangle.boundingBox([entry.rect for entry in group1]).calculateMargin()
                margin_bb2 = Rectangle.boundingBox([entry.rect for entry in group2]).calculateMargin()

                metric += margin_bb1 + margin_bb2

        if minMetric is None or metric < minMetric:
            minAxis = axis
            minMetric = metric

    return minAxis
