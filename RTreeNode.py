from Record import *
import numpy as np
from config import *


class Rectangle:
    """
    The smallest rectangle such that all points from given input
    lie inside that rectangle and sides of rectangle must be parallel
    to coordinate axis.
    """

    def __init__(self, points: list):
        self.min_coords = min_coords = np.min(points, axis=0)
        self.max_coords = max_coords = np.max(points, axis=0)

    def is_point_under_rectangle(self, point: Point) -> bool:
        for i, c in enumerate(point.coordinates):
            if not (c >= self.min_coords[i] and c <= self.max_coords[i]):
                return False
        return True


class RTreeEntry():
    """
    R-Tree entry containing either a pointer to a child Node instance or data.
    """

    def __init__(self, rect: Rectangle = None, child_id: int = None, data: Record = None):
        self.data = (data.blockId, data.slotId) if data else None
        self.rect = rect if rect else Rectangle(data.data.coordinates)
        self.child_id = child_id    # length = NODE_BLOCK_ID_SIZE

    @property
    def is_leaf(self):
        return self.child is None

    # TODO: to_string()


class RTreeNode(list):
    def __init__(self, capacity = BLOCKSIZE, block_id: int = 0, parent_id: int = None):
        super().__init__()
        self.capacity = capacity
        self._block_id = block_id
        self._parent_id = parent_id

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, value):
        self._block_id = value

    @property
    def parent_id(self):
        return self._parent_id

    def is_root(self):
        return self._block_id == 0

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value

    def toBytes(self):
        return bytearray("".join([str(item) for item in self]).encode("utf-8"))