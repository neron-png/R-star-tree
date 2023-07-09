import json
import config


class Record:
    
    def __init__(self, data_element):
        
        self.id = data_element.attrib.get("id")
        
        self.cor = []
        for c in config.COORDINATE_TAGS:
            self.cor.append(data_element.attrib.get(c))

        self.name = "Unknown"
        for t in data_element:
            if t.attrib.get("k") in config.NAME_TAGS:
                self.name = t.attrib.get("v") 
                break
    
        self._ = ""
        while self.__size__() < 256:
            self._ += "0"
        
    def __size__(self):
        return len(self.to_json())        

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None, separators= (',', ':')).encode('utf-8')
    