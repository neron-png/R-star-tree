from lxml import etree
from datetime import datetime
from Record import Record
import config
from Block import Block
import json


def getBlockFromDisk(blockID):

    with open(config.DATAFILE, 'r', encoding='utf-8') as datafile:
        datafile.seek(blockID*config.BLOCKSIZE)
        contents = datafile.read(config.BLOCKSIZE)
        
        if contents.startswith("["):
            contents = contents[1:]
        if contents.endswith("]"):
            contents = contents[:-1]
        if contents.endswith(","):
            contents = contents[:-1]
        
        print(contents)


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
                t = Record(element)
                
                if current_block.occupied() < block_slots_limit:
                    
                    # There is an empty slot that can host the parsing record
                    current_block.append(t)
                else:

                    # The block is full
                    # Fill it with dump '0's and write it in datafile 
                    current_block.fill_dump(1 if i == 0 else 0)
                    datafile.write(current_block.to_json())
                    datafile.write(bytes(",\n", 'utf-8'))

                    # Create a new block and store the parsing record there
                    block_index += 1
                    current_block = Block(block_index)
                    current_block.append(t)

            except Exception as E:
                with open("error_log",'+a') as log:
                    log.write(str(datetime.now()) + ": " + E.args[0] + "\n")
        
        # Create json object list closing
        datafile.seek(datafile.tell() - 2)
        datafile.write(bytes("]", 'utf-8'))


def writeRtreeToFile(rtree):
     with open(config.INDEXFILE, "w+") as indexFile:
         json.dump(rtree, indexFile)

