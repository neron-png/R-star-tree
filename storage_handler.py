from lxml import etree
import config
from record import Record


def parse_data_to_slot():
    pass

def write_blocks_to_datafile():
    # Parse the XML file

    with open(config.INPUTFILE, 'r') as file:
        data = file.read()

    parser = etree.XMLParser(encoding='utf-8', recover=True)
    data = "<data>" + data + "</data>"
    data = data.encode("utf-8")
    parsedData = etree.fromstring(data, parser=parser)

    # List to store the extracted nodes
    node_list = []

    # Iterate over each "node" element in the XML
    for element in parsedData.iter("node"):
        t = Record(element)
        print((t.to_json()))

        node_list.append(element)