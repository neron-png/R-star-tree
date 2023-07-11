import json
import config


class Record:

    def __init__(self, data_element):

        # Extract the needed data from the xml node attributes 
        # parsed in data_element parameter

        self.id = data_element.attrib.get("id")
        
        self.cor = []
        for c in config.COORDINATE_TAGS:
            self.cor.append(data_element.attrib.get(c))

        self.name = config.DEFAULT_POINT_NAME
        for t in data_element:
            if t.attrib.get("k") in config.NAME_TAGS:
                self.name = t.attrib.get("v") 
                break
    
        # The '_' attribute is used to give each record (block slot) the same size;
        # so each block contains the same number of slots (filled with records)

        # If the record is smaller than the fixed slot size, '_' fills with dump '0's
        self._ = ""
        while self.__size__() < config.RECORDSIZE:
            self._ += "0"

        # If the record is bigger than the fixed slot size, the name attribute gets cut
        while self.__size__() > config.RECORDSIZE and len(self.name) > 0:
            self.name = self.name[:-1]
        else:
            # It is mandatory for each data element to contain a name, such as the default
            if len(self.name) == 0:
                self.name = config.DEFAULT_POINT_NAME

            # If the name attribute (or any other) exceeds the size limit, abort record
            if self.__size__() > config.RECORDSIZE:
                raise Exception("Record (node) " + self.id + " exceeds the slot size limit")
        
    def __size__(self):
        return len(self.to_json())        

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None, separators= (',', ':')).encode('utf-8')
    