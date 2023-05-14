from collections.abc import Iterable

import node
import record
from config import *


class Block(list):
    def __init__(self, capacity = BLOCKSIZE, block_id = 0, parent_id = None):
        super().__init__()
        self.capacity = capacity
        self._block_id = block_id
        self._parent_id = parent_id

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, value):
        self._block_id = value

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value

    # For size checks, better not complicate it too much, but need to keep track when adding!

    # def append(self, item):
    #     if len(self.toBytes()) + len(bytearray(str(item).encode("utf-8"))) < self.capacity:
    #         super().append(item)
    #     else:
    #         raise ValueError("Block capacity exceeded.")
    #
    # def __iadd__(self, other):
    #     raise ValueError("+= Not supported because I'm lazy, use append() !")

    def toBytes(self):
        return bytearray("".join([str(record) for record in self]).encode("utf-8"))