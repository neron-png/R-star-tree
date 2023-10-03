
BLOCKSIZE = 32000
RECORDSIZE = 256
ENTRYSIZE = 256
INPUTFILE = "map.osm"
DATAFILE = "data.json"
INDEXFILE = "index.json"
m = 0.4 # Minimum Fill Ratio
P = 32 # Page 4 in paper, optimizing for large blocks when calculating overlap
SPLIT_P = 0.3 # Page 6 in paper, what percentage of the nodes in an overflown node to use in a reinsertion


COORDINATE_TAGS = ["lat", "lon"]

NAME_TAGS = ["name", "name:el", "name:en"]

DEFAULT_POINT_NAME = "Unknown"

MANTISSA = 10 ** 10


NUM_OF_COORDINATES = len(COORDINATE_TAGS)
COORDINATE_SIZE = 14
COORDINATES_INDEX_SIZE = len(str(NUM_OF_COORDINATES))

""" SESSION STORAGE """
""" These are global variables housed in the config file, used as stores """
OVERFLOWTREATMENT = {i: 0 for i in range(1000)}
