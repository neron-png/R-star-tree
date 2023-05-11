import sys

from config import *

'''
Represents a R-Tree node in disk (index-file object)
'''
class Node:
    def __init__(self, coordinates:list):
        self.data = coordinates
        self.blockId = 0
        self.slotId = 0
        self.childBlockId = 0
        self.childSlotId = 0

    def __str__(self):
        return f"""
        <node>
        <block-id>{ "{str:0{width}s}".format(width=NODE_BLOCK_ID_SIZE, str=str(int(self.blockId))[:NODE_BLOCK_ID_SIZE]) }</block-id>
        <slot-id>{ "{str:0{width}s}".format(width=NODE_SLOT_INDEX_SIZE, str=str(int(self.slotId))[:NODE_SLOT_INDEX_SIZE]) }</slot-id>
        <child-block-id>{ "{str:0{width}s}".format(width=NODE_BLOCK_ID_SIZE, str=str(int(self.childBlockId))[:NODE_BLOCK_ID_SIZE]) }</child-block-id>
        <child-slot-id>{ "{str:0{width}s}".format(width=NODE_SLOT_INDEX_SIZE, str=str(int(self.childSlotId))[:NODE_SLOT_INDEX_SIZE]) }</child-slot-id>
        <data>
       {"".join([f'<c{ "{str:0{width}s}".format(width=COORDINATES_INDEX_SIZE, str=str(i)[:COORDINATES_INDEX_SIZE]) }>{ "{str:0<{width}s}".format(width=COORDINATE_SIZE, str=str(float(coordinate))[:COORDINATE_SIZE]) }</c{ "{str:0{width}s}".format(width=COORDINATES_INDEX_SIZE, str=str(i)[:COORDINATES_INDEX_SIZE]) }>' for i, coordinate in enumerate(self.coordinates)])}
        </data>
        </node>
        """.replace("        ", "").replace("\n","")

NODE_SIZE = sys.getsizeof(str(Node(["1.0" for _ in range(NUM_OF_COORDINATES)])))