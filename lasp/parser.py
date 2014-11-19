from blocks import VersionBlock
from blocks import WellBlock
from blocks import CurveBlock
from blocks import ParameterBlock
from blocks import DataBlock
from errors import LasFormatException


class LasParser(object):
    _V = VersionBlock()
    _W = WellBlock()
    _C = CurveBlock()
    _P = ParameterBlock()
    _A = DataBlock()
    _comments = []

    def __init__(self, fname):
        block = None
        with open(fname) as fstream:
            for line in fstream:
                if line[0] == "~":
                    block = self.__getattribute__("_{}".format(line[1]))
                    block.title = line[1:]
                elif block:
                    block.parse(line)
                elif line[0] == "#":
                    self.comments.append(line[1:].strip())
                else:
                    raise LasFormatException("Block not specified")

    @property
    def comments(self):
        return self._comments

    @property
    def version(self):
        return self._V

    @property
    def well(self):
        return self._W

    @property
    def curve(self):
        return self._C

    @property
    def params(self):
        return self._P

    @property
    def data(self):
        return self._A
