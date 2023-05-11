from io import StringIO
from config import *

'''
Represents a n-D point
'''
class Point:
    def __init__(self, name:str, id:str, coordinates:list):
        self.locName = "{:<128}".format(name[:128])
        self.locId = "{:<10}".format(id[:10])
        self.coordinates = coordinates
    
    def __str__(self):
        return f"""
        <id>{ self.locId }</id>
        <name>{ self.locName }</name>
        {"".join([f'<c{ "{number:0{width}d}".format(width=COORDINATES_INDEX_SIZE, number=i) }>{ coordinate }</c{ "{number:0{width}d}".format(width=COORDINATES_INDEX_SIZE, number=i) }>' for i, coordinate in enumerate(self.coordinates)])}    # Assumption for sizes max coordinates n
        """.replace("\n", "")

'''
Represents a stored data record in disk (data-file object)
'''
class Record:
    def __init__(self, point:Point):
        self.data = point
        self.blockId = "{number:0{width}d}".format(width=BLOCK_INDEX_SIZE, number=0)
        self.slotId = "{number:0{width}d}".format(width=RECORD_SLOT_INDEX_SIZE, number=0)

    def __str__(self):
        return f"""\
        <record>\
        <block-id>{ self.blockId }</block-id>\
        <slot-id>{ self.slotId }</slot-id>\
        <data>{ str(self.data) }</data>\
        </record>\
        """.replace(" ", "")

    def setBlockId(self, id:int):
        self.blockId = "{number:0{width}d}".format(width=BLOCK_INDEX_SIZE, number=id)

    def setSlotId(self, id:int):
        self.slotIdId = "{number:0{width}d}".format(width=RECORD_SLOT_INDEX_SIZE, number=id)

    @staticmethod
    def parseXMLtoRecordsList(block:str) -> list:
        from lxml import etree
        records = []
        parser = etree.XMLParser(encoding='utf-8', recover=True)
        block = "<a>" + block + "</a>" #Tricking it to believe it's validly formed XML
        block = block.encode("utf-8")

        parsedBlock = etree.fromstring(block, parser=parser)


        names = parsedBlock.xpath('//node/tag[@k="name"]/@v')
        ids = parsedBlock.xpath('//node[tag[@k="name"]]/@id')
        LATcoordinates = parsedBlock.xpath('//node[tag[@k="name"]]/@lat')
        LONcoordinates = parsedBlock.xpath('//node[tag[@k="name"]]/@lon')
        for i in range(len(LATcoordinates)):
            rec = Record(Point(names[i],ids[i],[LATcoordinates[i],LONcoordinates[i]]))
            records.append(rec)

        ids = parsedBlock.xpath('//node/@id')
        LATcoordinates = parsedBlock.xpath('//node/@lat')
        LONcoordinates = parsedBlock.xpath('//node/@lon')
        for i in range(len(LONcoordinates)):
            rec = Record(Point("unknown",ids[i],[LATcoordinates[i],LONcoordinates[i]]))
            records.append(rec)

        return records
