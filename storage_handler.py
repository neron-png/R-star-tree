from lxml import etree
from datetime import datetime
from record import Record
import config


def write_blocks_to_datafile():
    
    # Parse the XML raw-data input file 
    # and create the block-defined datafile

    # Store in temporary in a variable the raw-data
    with open(config.INPUTFILE, 'r') as file:
        data = file.read()

    # Initialize the xml parser and parse the raw-data variable 
    parser = etree.XMLParser(encoding='utf-8', recover=True)
    data = "<data>" + data + "</data>"
    data = data.encode("utf-8")
    parsedData = etree.fromstring(data, parser=parser)


    # List to store the extracted nodes
    node_list = []

    # Iterate over each "node" element in the XML
    for element in parsedData.iter("node"):
        try:
            t = Record(element)
            node_list.append(t)
        except Exception as E:
            with open("error_log",'+a') as log:
                log.write(str(datetime.now()) + ": " + E.args[0] + "\n")