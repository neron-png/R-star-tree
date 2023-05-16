import sys

from config import *

'''
Represents a n-D point
'''
class Point:
    def __init__(self, name: str, pointId: str, coordinates: list):
        self.pointName = name[:POINT_NAME_SIZE]
        self.pointId = int(pointId[:POINT_ID_SIZE])
        self.coordinates = coordinates

    def __str__(self):

        # Fix for name having differing size in Greek:
        nameRealSize = len(self.pointName.encode('utf-8'))

        # Trying to make it so it treats greek based on it's size in bytes
        # In case it breaks, it replaces it with [REDACTED] as a catchall
        try:
            CorrName = f"{ self.pointName.encode('utf-8')[:POINT_NAME_SIZE].decode('utf-8') + '_'*(POINT_NAME_SIZE-nameRealSize) }"
        except Exception as e:
            CorrName = "{str:_<{width}s}".format(width=POINT_NAME_SIZE, str="[REDACTED]"[:POINT_NAME_SIZE])
            # "{str:_<{width}s}".format(width=POINT_NAME_SIZE, str=self.pointName[:POINT_NAME_SIZE])

        return f"""
        <id>{ "{str:0>{width}s}".format(width=POINT_ID_SIZE, str=str(int(self.pointId))[:POINT_ID_SIZE]) }</id>
        <name>{ CorrName }</name>
        {"".join([f'<c{ "{str:0>{width}s}".format(width=COORDINATES_INDEX_SIZE, str=str(i)[:COORDINATES_INDEX_SIZE]) }>{ "{str:0<{width}s}".format(width=COORDINATE_SIZE, str=str(coordinate)[:COORDINATE_SIZE]) }</c{ "{str:0>{width}s}".format(width=COORDINATES_INDEX_SIZE, str=str(i)[:COORDINATES_INDEX_SIZE]) }>' for i, coordinate in enumerate(self.coordinates)])}
        """.replace("\n", "")

'''
Represents a stored data record in disk (data-file object)
'''
class Record:
    def __init__(self, point: Point):
        self.data = point
        self.blockId = 0
        self.slotId = 0

    def __str__(self):
        return f"""
        <record>
        <block-id>{ "{str:0>{width}s}".format(width=RECORD_BLOCK_ID_SIZE, str=str(int(self.blockId))[:RECORD_BLOCK_ID_SIZE]) }</block-id>
        <slot-id>{ "{str:0>{width}s}".format(width=RECORD_SLOT_INDEX_SIZE, str=str(int(self.slotId))[:RECORD_SLOT_INDEX_SIZE]) }</slot-id>
        <data>{ self.data }</data>
        </record>
        """.replace("        ", "").replace("\n","")

    @staticmethod
    def parseXMLToRecordsList(block: str) -> list:
        from lxml import etree
        records = []
        parser = etree.XMLParser(encoding='utf-8', recover=True)
        block = "<block>" + block + "</block>" #Tricking it to believe it's validly formed XML
        block = block.encode("utf-8")

        parsedBlock = etree.fromstring(block, parser=parser)

        names = parsedBlock.xpath('//node/tag[@k="name"]/@v')
        ids = parsedBlock.xpath('//node[tag[@k="name"]]/@id')
        LATcoordinates = parsedBlock.xpath('//node[tag[@k="name"]]/@lat')
        LONcoordinates = parsedBlock.xpath('//node[tag[@k="name"]]/@lon')
        for i in range(len(LATcoordinates)):
            record = Record(Point(names[i],ids[i],[LATcoordinates[i],LONcoordinates[i]]))
            records.append(record)

        ids = parsedBlock.xpath('//node/@id')
        LATcoordinates = parsedBlock.xpath('//node/@lat')
        LONcoordinates = parsedBlock.xpath('//node/@lon')
        for i in range(len(LONcoordinates)):
            record = Record(Point("unknown",ids[i],[LATcoordinates[i],LONcoordinates[i]]))
            records.append(record)

        return records

    @staticmethod
    def parseBlockToRecordsList(block: str) -> list:
        from lxml import etree
        records = []
        parser = etree.XMLParser(encoding='utf-8', recover=True)

        block = "<a>" + block + "</a>"  # Tricking it to believe it's validly formed XML
        block = block.encode("utf-8")

        parsedBlock = etree.fromstring(block, parser=parser)

        block_ids = parsedBlock.xpath('//block-id')
        slot_ids = parsedBlock.xpath('//slot-id')

        point_ids = parsedBlock.xpath('//id')
        names = parsedBlock.xpath('//name')

        coordinates = []
        for i in range(NUM_OF_COORDINATES):
            coordinates.append(parsedBlock.xpath("//c" + str(i)))

        for i in range(len(block_ids)):
            record = Record(Point(names[i].text, point_ids[i].text, [float(coordinates[j][i].text) for j in range(len(coordinates))]))
            record.blockId = block_ids[i].text
            record.slotId = slot_ids[i].text
            records.append(record)

        return records

RECORD_SIZE = len(bytearray(str(Record(Point("dummy","0",["1.0" for _ in range(NUM_OF_COORDINATES)]))).encode("utf-8")))