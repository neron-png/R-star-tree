import sys

from config import *

class Node:
    def __init__(self, coordinates:list):
        self.data = coordinates
        self.blockId = 0
        self.slotId = 0
        # self.childBlockId = 0
        # self.childSlotId = 0

    def __str__(self):
        return f"""
        <node>
        <block-id>{ "{str:0>{width}s}".format(width=NODE_BLOCK_ID_SIZE, str=str(int(self.blockId))[:NODE_BLOCK_ID_SIZE]) }</block-id>
        <slot-id>{ "{str:0>{width}s}".format(width=NODE_SLOT_INDEX_SIZE, str=str(int(self.slotId))[:NODE_SLOT_INDEX_SIZE]) }</slot-id>
        <data>
       {"".join([f'<c{ "{str:0>{width}s}".format(width=COORDINATES_INDEX_SIZE, str=str(i)[:COORDINATES_INDEX_SIZE]) }>{ "{str:0<{width}s}".format(width=COORDINATE_SIZE, str=str(float(coordinate))[:COORDINATE_SIZE]) }</c{ "{str:0>{width}s}".format(width=COORDINATES_INDEX_SIZE, str=str(i)[:COORDINATES_INDEX_SIZE]) }>' for i, coordinate in enumerate(self.data)])}
        </data>
        </node>
        """.replace("        ", "").replace("\n","")

        # < child - block - id > {"{str:0>{width}s}".format(width=NODE_BLOCK_ID_SIZE, str=str(int(self.childBlockId))[
        #                                                                                 :NODE_BLOCK_ID_SIZE])} < / child - block - id >
        # < child - slot - id > {"{str:0>{width}s}".format(width=NODE_SLOT_INDEX_SIZE, str=str(int(self.childSlotId))[
        #                                                                                  :NODE_SLOT_INDEX_SIZE])} < / child - slot - id >

    def parseBlockToNodeList(block:str) -> list:
        from lxml import etree
        nodes = []
        parser = etree.XMLParser(encoding='utf-8', recover=True)

        parsedBlock = etree.fromstring(block, parser=parser)

        block_ids = parsedBlock.xpath('//block-id')
        slot_ids = parsedBlock.xpath('//slot-id')

        # child_block_ids = parsedBlock.xpath('//child-block-id')
        # child_slot_ids = parsedBlock.xpath('//child-slot-id')

        coordinates = []
        for i in range(NUM_OF_COORDINATES):
            coordinates.append(parsedBlock.xpath("//c" + str(i)))

        for i in range(len(block_ids)):
            node = Node(coordinates[i])
            node.blockId = block_ids[i]
            node.slotId = slot_ids[i]
            # node.childBlockId = child_block_ids[i]
            # node.childSlotId = child_slot_ids[i]
            nodes.append(node)

        return nodes

NODE_SIZE = sys.getsizeof(str(Node(["1.0" for _ in range(NUM_OF_COORDINATES)])))