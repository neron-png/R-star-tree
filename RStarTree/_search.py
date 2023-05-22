from storageHandler import *
from config import *

def search_record(self, p: Point) -> Record:
    """ Find a point indexed by the RTree """

    data_ref = self.find_path(self.root, p)[-1][-1]
    return fetchBlock(DATAFILE, data_ref[0])[data_ref[1]]