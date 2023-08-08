
BLOCKSIZE = 32000
BLOCKSIZE = 1024 #FIXME: temporary
RECORDSIZE = 256
ENTRYSIZE = 256
INPUTFILE = "map.osm"
DATAFILE = "data.json"
INDEXFILE = "index.json"
m = 0.4 # Minimum Fill Ratio #TODO #FIXME update Bulkload to accomodate this
P = 32 # Page 4 in paper, optimizing for large blocks when calculating overlap


COORDINATE_TAGS = ["lat", "lon"]

NAME_TAGS = ["name", "name:el", "name:en"]

DEFAULT_POINT_NAME = "Unknown"

MANTISSA = 10 ** 10

FILEHEADER = """
<header>
<type>{0}</type>
<records>0</records>
<lastrecord>0</lastrecord>
</header>
"""

NUM_OF_COORDINATES = len(COORDINATE_TAGS)
COORDINATE_SIZE = 14
COORDINATES_INDEX_SIZE = len(str(NUM_OF_COORDINATES))

RECORD_BLOCK_ID_SIZE = 5
RECORD_SLOT_INDEX_SIZE = 4

NODE_ID_SIZE = 5
NODE_SLOT_INDEX_SIZE = 4
NODE_ENTRIES_NUM = 10 ** NODE_SLOT_INDEX_SIZE

NODE_MIN_ENTRIES = NODE_ENTRIES_NUM // 2

POINT_NAME_SIZE = 32
POINT_ID_SIZE = 10

# RTREE PARAMS
NODE_SAMPLE = 20

MAX_FILL_CAPACITY_PERCENTAGE = 1.0
MIN_FILL_CAPACITY_PERCENTAGE = 0.4 # Suggested by the paper
REINSERT_PERCENTAGE = 0.3
