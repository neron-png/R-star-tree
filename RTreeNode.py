import sys

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
        self.min_coords = np.min(points, axis=0)
        self.max_coords = np.max(points, axis=0)

    def is_point_under_rectangle(self, point: Point) -> bool:
        for i, c in enumerate(point.coordinates):
            if not (c >= self.min_coords[i] and c <= self.max_coords[i]):
                return False
        return True

    def __str__(self):
        minC, maxC = [], []
        for c in list(self.min_coords):
            minC.append("{str:0<{width}s}".format(width=COORDINATE_SIZE, str=str(c)))
        for c in list(self.max_coords):
            maxC.append("{str:0<{width}s}".format(width=COORDINATE_SIZE, str=str(c)))

        return f"""{minC},{maxC}""".replace("\'","")


class RTreeEntry():
    """
    R-Tree entry containing either a pointer to a child Node instance or data.
    """

    def __init__(self, rect: Rectangle = None, child_id: int = None, data: Record = None):
        self.rect = rect if rect else Rectangle([data.data.coordinates])
        self.data = (data.blockId, data.slotId) if data else None
        self.child_id = child_id

    @property
    def is_leaf(self):
        return self.child is None

    def __str__(self):
        return f"""
                <entry>
                <rect> 
                    { self.rect } 
                </rect>
                <data>
                <block-id> 
                    {"{str:0>{width}s}".format(width=NODE_BLOCK_ID_SIZE, str=str(self.data[0] if self.data is not None else "")[:NODE_BLOCK_ID_SIZE])}
                </block-id>
                <slot-id>
                    {"{str:0>{width}s}".format(width=NODE_SLOT_INDEX_SIZE, str=str(self.data[1] if self.data is not None else "")[:NODE_BLOCK_ID_SIZE])}
                </slot-id>
                </data>
                <child-id>{"{str:0>{width}s}".format(width=NODE_BLOCK_ID_SIZE, str=str(self.child_id if self.child_id is not None else "")[:NODE_SLOT_INDEX_SIZE])}</child-id>
                </entry>
                """.replace(" ", "").replace("\n", "")

    def toBytes(self):
        return bytearray("".join([item for item in str(self)]).encode("utf-8"))


ENTRY_SIZE = sys.getsizeof(str(RTreeEntry(Rectangle([[1.0 for _ in range(NUM_OF_COORDINATES)]]),None,None)),'utf-8')


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