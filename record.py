'''
Represents a n-D point
'''
class Point:
    def __init__(self, name:str, id:str, coordinates:list):
        self.locName = name[10]
        self.locId = id[0:128]
        self.coordinates = coordinates
    
    def __str__(self):
        return f"""
        <id>{ self.locId }</id>
        <name>{ self.locName }</name>
        {"".join(["<c" + i + ">" + coordinate + "</c" + i + ">" for i, coordinate in enumerate(self.coordinates)])}
        """

'''
Represents a stored data record in disk
'''
class Record:
    def __init__(self, point:Point):
        self.data = point
        self.blockId = 0;
        self.slotId = 0;
    
    def __str__(self):
        return f"""
        <record>{ self.blockId }
        <block-id>{ self.blockId }</block-id>
        <slot-id>{ self.slotId }</slot-id>
        <data>{ str(self.data) }</data>
        </record>
        """
    