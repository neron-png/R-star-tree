
BLOCKSIZE = 32000
INPUTFILE = "map.osm"
DATAFILE = "data.xml"
INDEXFILE = "index.xml"

FILEHEADER = """
<header>
<type>{0}</type>
<records>0</records>
<lastrecord>0</lastrecord>
</header>
"""

RECORD_INDEX_SIZE = 10

NUM_OF_COORDINATES = 2
COORDINATE_SIZE = 10
COORDINATES_INDEX_SIZE = len(str(NUM_OF_COORDINATES))

BLOCK_INDEX_SIZE = 10
RECORD_SLOT_INDEX_SIZE = 10
