import sys
import storageHandler as sh
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

    def get_min_coords(self):
        return self.min_coords

    def get_max_coords(self):
        return self.max_coords

    def contains_point(self, point: Point) -> bool:
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

    def calculateSize(self):
        size = 1
        for i, _ in enumerate(self.max_coords):
            size *= self.max_coords[i] - self.min_coords[i]

        return size

    def calculateExpansion(self, point: Point):
        temp_min_coords = self.min_coords
        temp_max_coords = self.max_coords

        if self.contains_point(point):
            return 0
        else:
            newSize = 1
            for i, coordinate in enumerate(point.coordinates):
                if coordinate < temp_min_coords[i]:
                    temp_min_coords[i] = coordinate
                elif coordinate > temp_max_coords[i]:
                    temp_max_coords[i] = coordinate
                newSize *= temp_max_coords[i]-temp_min_coords[i]

        return newSize - self.calculateSize()

    def includePoint(self, point: Point):
        if self.contains_point(point):
            return
        else:
            self.min_coords = np.min([point.coordinates, self.min_coords])
            self.max_coords = np.max([point.coordinates, self.max_coords])

    def intersectSize(self, otherRectangle):

        rect1 = self
        rect2 = otherRectangle

        # Calculate the maximum of the lower bounds and the minimum of the upper bounds along each dimension
        overlap_lengths = []
        for i in range(len(rect1.max_coords)):
            lower_bound = max(rect1.min_coords[i], rect2.min_coords[i])
            upper_bound = min(rect1.max_coords[i], rect2.max_coords[i])

            overlap_length = upper_bound - lower_bound
            if overlap_length < 0:
                return 0  # Cubes do not overlap, overlap length is negative
            else:
                overlap_lengths.append(overlap_length)

        # Calculate the overlap volume
        overlap_volume = 1
        for length in overlap_lengths:
            overlap_volume *= length

        return overlap_volume


class RTreeEntry():
    """
    R-Tree entry containing either a pointer to a child Node instance or data.
    """

    def __init__(self, rect: Rectangle = None, child_id: int = None, data: Record = None):
        self.rect = rect if rect else Rectangle([data.data.coordinates])
        self.data = (data.blockId, data.slotId) if data else None
        self.child_id = child_id

    @property
    def is_leaf_entry(self) -> bool:
        return self.child_id is None

    def __str__(self):
        return f"""
                <entry>
                <rect> 
                    { self.rect } 
                </rect>
                <data>
                <block-id> 
                    {"{str:0>{width}s}".format(width=NODE_ID_SIZE, str=str(self.data[0] if self.data is not None else "")[:NODE_ID_SIZE])}
                </block-id>
                <slot-id>
                    {"{str:0>{width}s}".format(width=NODE_SLOT_INDEX_SIZE, str=str(self.data[1] if self.data is not None else "")[:NODE_ID_SIZE])}
                </slot-id>
                </data>
                <child-id>{"{str:0>{width}s}".format(width=NODE_ID_SIZE, str=str(self.child_id if self.child_id is not None else "")[:NODE_SLOT_INDEX_SIZE])}</child-id>
                </entry>
                """.replace(" ", "").replace("\n", "")

    def calculateExpansion(self, record: Record):
        return self.rect.calculateExpansion(record.data)

    def recalculateRectangle(self, record:Record):
        self.rect.includePoint(record.data)

    def toBytes(self):
        return bytearray("".join([item for item in str(self)]).encode("utf-8"))


# ENTRY_SIZE = sys.getsizeof(str(RTreeEntry(Rectangle([[1.0 for _ in range(NUM_OF_COORDINATES)]]),None,None)).encode('utf-8'))
ENTRY_SIZE = len(bytearray((str(RTreeEntry(Rectangle([[1.0 for _ in range(NUM_OF_COORDINATES)]]),None,None)).encode('utf-8'))))

class RTreeNode(list):
    def __init__(self, capacity = BLOCKSIZE, block_id: int = 0, parent_id: int = None):
        super().__init__()
        self.capacity = capacity
        self._block_id = block_id
        self._parent_id = parent_id

    def fromFileID(self, blockID: int, parentID: int = None):
        self.__init__(block_id=blockID, parent_id=parentID)
        self.append(sh.fetchBlock(INDEXFILE, blockID))



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

    @property
    def is_leaf_node(self) -> bool:
        for item in self:
            if item is RTreeEntry and item.is_leaf_entry:
                return True
        return False

    def parseBlockToEntryList(block: str) -> list:
        from lxml import etree
        entries = []
        parser = etree.XMLParser(encoding='utf-8', recover=True)

        parsedBlock = etree.fromstring(block, parser=parser)

        rects = parsedBlock.xpath('//rect')
        block_ids = parsedBlock.xpath('//block-id')
        slot_ids = parsedBlock.xpath('//slot-id')
        child_ids = parsedBlock.xpath('//child-id')

        for i in range(len(rects)):
            entry = RTreeEntry(Rectangle([rects[i].text]),int(child_ids[i].text),(block_ids[i].text,slot_ids[i].text))
            entries.append(entry)

        return entries

    def toBytes(self):
        return bytearray("".join([str(item) for item in self]).encode("utf-8"))

    def isOversized(self):
        return self.capacity >= ENTRY_SIZE*len(self)
