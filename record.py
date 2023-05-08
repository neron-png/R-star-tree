'''
Represents a n-D point
'''
class Point:
    def __init__(self, name:str, id:str, coordinates:list):
        self.locName = name[0:10]
        self.locId = id[0:128]
        self.coordinates = coordinates
    
    def __str__(self):
        return f"""
        <id>{ self.locId }</id>
        <name>{ self.locName }</name>
        {"".join([f'<c{i}>{coordinate}</c{i}>' for i, coordinate in enumerate(self.coordinates)])}
        """.replace("\n", "")

'''
Represents a stored data record in disk
'''
class Record:
    def __init__(self, point:Point):
        self.data = point
        self.blockId = 0
        self.slotId = 0
    
    def __str__(self):
        return f"""\
        <record>\
        <block-id>{ self.blockId }</block-id>\
        <slot-id>{ self.slotId }</slot-id>\
        <data>{ str(self.data) }</data>\
        </record>\
        """.replace(" ", "")
    
    @staticmethod
    def parseXMLtoRecordsList(block:str) -> list:
        from lxml import etree
        records = []  
        names = etree.fromstring(block).xpath('//node/tag[@k=\'name:en\']')
        ids = etree.fromstring(block).xpath('//node/tag[@k="name:en"]/../@id')
        LATcoordinates = etree.fromstring(block).xpath('//node/tag[@k="name:en"]/../@lat')
        LONcoordinates = etree.fromstring(block).xpath('//node/tag[@k="name:en"]/../@lon')
        for i in range(len(LATcoordinates)):
            records.append(Record(Point(names[i],ids[i],[LATcoordinates[i],LONcoordinates[i]])))
        return records
