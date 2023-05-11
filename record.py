from io import StringIO

'''
Represents a n-D point
'''
class Point:
    def __init__(self, name:str, id:str, coordinates:list):
        self.locName = name[0:128]
        self.locId = id[0:10]
        self.coordinates = coordinates
    
    def __str__(self):
        return f"""
        <id>{ self.locId }</id>
        <name>{ self.locName }</name>
        {"".join([f'<c{i}>{coordinate}</c{i}>' for i, coordinate in enumerate(self.coordinates)])}
        """.replace("\n", "")

'''
Represents a stored data record in disk (data-file object)
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
