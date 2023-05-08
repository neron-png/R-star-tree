'''
Represents a R-Tree node
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
        <block-id>{ self.blockId }</block-id>
        <slot-id>{ self.slotId }</slot-id>
        <child-block-id>{ self.childBlockId }</child-block-id>
        <child-slot-id>{ self.childSlotId }</child-slot-id>
        <data>
        {"".join(["<c" + i + ">" + coordinate + "</c" + i + ">" for i, coordinate in enumerate(self.coordinates)])}
        </node>
        """