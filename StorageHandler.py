from lxml import etree
from datetime import datetime
from Record import Record
import config
from Block import Block
import json
import itertools


def searchByID(id):
    """
    @params: No.de id, id of node to be deleted
        @return: (True, record) if found | (False, "Reason") if not succeeded
    """
    item = None

    flag = False
    for i in itertools.count(start=1):
        if flag:
            break
        try:
            block = getBlockFromDisk(i)
            for record in block["slots"]:
                if record["id"] == id:
                    item = record
                    flag = True
                    break

        except Exception as e:
            return (False, "Item not found")
            break
    
    return (True, item)


def getBlockFromDisk(blockID):
    blockID -=1
    with open(config.DATAFILE, 'r', encoding='utf-8') as datafile:
        datafile.seek(blockID*config.BLOCKSIZE)
        contents = datafile.read(config.BLOCKSIZE)
        print(contents)
        if contents.startswith("["):
            contents = contents[1:]
        if contents.startswith(","):
            contents = contents[1:]
        if contents.endswith("]"):
            contents = contents[:-1]
        if contents.endswith(","):
            contents = contents[:-1]
        
        return json.loads(contents)


def writeBlockToDisk(blockID, block):
    contents = json.dumps(block)
    if blockID == 0 :
        pass # "[" + block
        #TODO padd to match the blocksize

    with open(config.DATAFILE, 'w', encoding='utf-8') as datafile:
        datafile.seek(blockID*config.BLOCKSIZE)
        contents = datafile.read(config.BLOCKSIZE)


def write_blocks_to_datafile():
    
    # Parse the XML raw-data input file 
    # and create the block-defined datafile

    # Store in temporary in a variable the raw-data
    with open(config.INPUTFILE, 'r', encoding='utf-8') as file:
        data = file.read()

    # Initialize the xml parser and parse the raw-data variable 
    parser = etree.XMLParser(encoding='utf-8', recover=True)
    data = "<data>" + data + "</data>"
    data = data.encode('utf-8')
    parsedData = etree.fromstring(data, parser=parser)


    # First block of datafile where the parsed data will be stored at
    block_index = 1
    current_block = Block(block_index)

    with open(config.DATAFILE, 'wb+') as datafile:
        
        # Create json object list opening
        datafile.write(bytes("[", 'utf-8'))

        # Compute how many slots/records can a block host
        block_slots_limit = config.BLOCKSIZE // config.RECORDSIZE - 1

        for i, element in enumerate(parsedData.iter("node")):
            try:
                
                # Parse raw-data element to Record object
                t = Record()
                t.setFromData(element)
                
                if current_block.occupied() < block_slots_limit:
                    
                    # There is an empty slot that can host the parsing record
                    current_block.append(t)
                else:

                    # The block is full
                    # Fill it with dump '0's and write it in datafile 
                    current_block.fill_dump(1 if i == 0 else 0)
                    datafile.write(current_block.to_json())
                    datafile.write(bytes(",", 'utf-8'))

                    # Create a new block and store the parsing record there
                    block_index += 1
                    current_block = Block(block_index)
                    current_block.append(t)

            except Exception as E:
                with open("error_log",'+a') as log:
                    log.write(str(datetime.now()) + ": " + E.args[0] + "\n")
        
        # Create json object list closing
        datafile.seek(datafile.tell() - 1)
        datafile.write(bytes("]", 'utf-8'))


def writeRtreeToFile(rtree):
     with open(config.INDEXFILE, "w") as indexFile:
         json.dump(rtree, indexFile)


def writeRecordToDisk(r: Record) -> int:
    # Fetch datafile to get a list of blocks as python dict
    with open(config.DATAFILE, 'r') as file:
        data = json.load(file)

    # Compute how many slots/records can a block host
    block_slots_limit = config.BLOCKSIZE // config.RECORDSIZE - 1
    
    placed = False
    bId = -1

    # Iterate through blocks of datafile and try to find a
    # block with empty slots to put there the record (r)
    for i, block in enumerate(data):
        if len(block["slots"]) >= block_slots_limit:
            continue
        else:
            # Create a copy of the selected block
            # where the record will be appended
            tempBlock = Block(block["id"])
            tempBlock.slots.extend(block["slots"])
            tempBlock.slots.append(r)
            tempBlock.fill_dump(1 if i == 0 else 0)
            
            block["slots"] = tempBlock.slots
            block["_"] = tempBlock._

            bId = block["id"]
            placed = True
            break
    
    # If the record (r) does not fit in any existing block
    # create a new block and append it there
    if not placed:
        if len(data) > 0:
            bId = data[-1]["id"] + 1
        else:
            bId = 1
        
        newBlock = Block(bId)
        newBlock.append(r)
        newBlock.fill_dump(1 if bId == 1 else 0)
        data.append(newBlock)

    with open(config.DATAFILE, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, default=lambda o: o.__dict__, indent=None, separators=(',', ':')))
    
    # Return the block's id where the record (r) was appended
    return bId


def fetchRecordFromDisk(bId: int, sId: int) -> dict:
    # Fetch datafile to get a list of blocks as python dict
    with open(config.DATAFILE, 'r') as file:
        data = json.load(file)
    
    # Iterate through blocks of datafile and try to find 
    # the block that contains the requested record (slot)
    for j, block in enumerate(data):
        if block["id"] == bId:
            for i, slot in enumerate(block["slots"]):
                if slot["id"] == sId:
                    return slot
    
    return {}


def deleteRecordFromDisk(bId: int, sId: int) -> bool:
    # Fetch datafile to get a list of blocks as python dict
    with open(config.DATAFILE, 'r') as file:
        data = json.load(file)
    
    result = False

    # Iterate through blocks of datafile and try to find 
    # the block that contains the requested record (slot)
    for j, block in enumerate(data):

        if block["id"] == bId:

            for i, slot in enumerate(block["slots"]):
                if slot["id"] == sId:
                    block["slots"].pop(i)
                    result = True
        
                    # Create a copy of the selected block to set the correct resizement
                    tempBlock = Block(bId)
                    tempBlock.slots.extend(block["slots"])
                    tempBlock.fill_dump(1 if j == 0 else 0)
                    
                    block["_"] = tempBlock._
                    
                    with open(config.DATAFILE, 'w', encoding='utf-8') as file:
                        file.write(json.dumps(data, default=lambda o: o.__dict__, indent=None, separators=(',', ':')))
                    
                    break
    return result