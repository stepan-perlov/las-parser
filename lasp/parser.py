import traceback
from blocks import VersionBlock
from blocks import WellBlock
from blocks import CurveBlock
from blocks import ParameterBlock
from blocks import DataBlock
from errors import LasFormatException


class LasParser(object):

    def __init__(self, fname):
        self.errors = []
        self._V = VersionBlock()
        self._W = WellBlock()
        self._C = CurveBlock()
        self._P = ParameterBlock()
        self._A = DataBlock()
        self._comments = []

        block = None
        with open(fname) as fstream:
            for line in fstream:
                try:
                    if line[0] == "~":
                        block = self.__getattribute__("_{}".format(line[1]))
                        block.title = line[1:]
                    elif block:
                        block.parse(line)
                    elif line[0] == "#":
                        self.comments.append(line[1:].strip())
                    else:
                        raise LasFormatException("Block not specified")
                except LasFormatException as e:
                    raise e
                except Exception:
                    self.errors.append(traceback.format_exc())

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
