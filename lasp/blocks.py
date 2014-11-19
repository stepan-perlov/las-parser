import re
from abc import ABCMeta, abstractmethod

from errors import LasFormatException
from errors import VersionBlockException
from errors import WellBlockException
from errors import CurveBlockException
from errors import ParameterBlockException
from errors import OtherBlockException
from errors import DataBlockException


class BlockBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._title = None
        self._header = None

    @abstractmethod
    def parse(self, line):
        pass


class InformationBlock(BlockBase):
    __metaclass__ = ABCMeta

    def __init__(self):
        BlockBase.__init__(self)
        self._linenum = 0
        self._regexp = None
        self._data = {}
        self._comments = []
        self._data_subh = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not self._title:
            self._title = value.strip()

    @property
    def comments(self):
        return self._comments

    @property
    def data(self):
        return self._data

    def get(self, key):
        return self._data.get(key.upper(), None)

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, line):
        if not self._header:
            headers = re.split(r"\s*\.\s*|\s{3,}", line[1:].strip())
            if not headers[1].lower() == "unit":
                headers = [headers[0], "UNIT"] + headers[1:]
            if len(headers) != 4:
                if "description" in headers[2].lower():
                    headers.append(headers[2])
                    headers[2] = "Data"
                else:
                    headers.append("Description")

            self._header = {
                "name": re.sub(r"\s+", "_", headers[0].strip()),
                "unit": re.sub(r"\s+", "_", headers[1].strip()),
                "data": re.sub(r"\s+", "_", headers[2].strip()),
                "comment": re.sub(r"\s+", "_", headers[3].strip()),
                "without_name": [re.sub(r"\s+", "_", h.strip()) for h in headers[1:]]
            }

    @property
    def data_subh(self):
        return self._data_subh

    @data_subh.setter
    def data_subh(self, line):
        if not self._data_subh:
            data_subh = re.split(r"\.|\s+", line.strip())[2]
            split = re.split(r"-+", data_subh)
            if split != ["", ""]:
                self._data_subh = split

    @property
    def regexp(self):
        if not self._regexp:
            regexp_base = [
                "\s*",
                "(?P<{}>".format(self.header["name"]),
                    "\w+|\s{{0}}",
                ")",
                "\s*\.\s*",
                "(?P<{}>".format(self.header["unit"]),
                    "[\w\/\.\\\\]+|\s{{0}}",
                ")",
                "\s{{3,}}",
                "{data_group}",
                "\s*:\s*",
                "(?P<{}>".format(self.header["comment"]),
                    ".*[\w\d]|\s{{0}}",
                ")",
                "\s*"
            ]
            if self.data_subh:
                data_group = "\s+".join([
                    "(?P<{}>[\w\d\.\-,\\\\/]+|\s{{0}})".format(name)
                    for name in self.data_subh
                ])
            else:
                data_group = "(?P<{}>.*[^\s]|\s{{0}})".format(self.header["data"])
            regexp_str = "".join(regexp_base).format(data_group=data_group)
            self._regexp = re.compile(regexp_str)
        return self._regexp

    def parse(self, line):
        if line[0] == "#" and self._linenum == 0:
            self.header = line
        elif line[0] == "#" and self._linenum == 1:
            self.data_subh = line
        elif line[0] == "#":
            self._comments.append(line[1:].strip())
        else:
            result = self.regexp.match(line.strip()).groupdict()
            if result[self.header["name"]]:
                key = result[self.header["name"]].upper()
                obj = self.data[key] = {self.header["data"]: {}}
                for key, value in result.iteritems():
                    if key in self.header["without_name"]:
                        obj[key] = value or None
                    elif key in self.data_subh:
                        obj[self.header["data"]][key] = value or None
        self._linenum += 1

class VersionBlock(InformationBlock):
    def __init__(self):
        InformationBlock.__init__(self)
        regexp = [
            "\s*",
            "(?P<name>",
                "\w+|\s{0}",
            ")",
            "\s*\.\s{3,}",
            "(?P<value>",
                ".*[\w\d]|\s{0}",
            ")",
            "\s*:\s*",
            "(?P<comment>",
                ".*[^\s]|\s{0}",
            ")",
            "\s*"
        ]
        self._regexp = re.compile("".join(regexp))
        self._header = {
            "name": "name",
            "data": "value",
            "without_name": ["value", "comment"]
        }

class WellBlock(InformationBlock):
    pass

class CurveBlock(InformationBlock):
    pass

class ParameterBlock(InformationBlock):
    pass

class OtherBlock(InformationBlock):
    pass

class DataBlock(BlockBase):
    _set = []

    @property
    def set(self):
        return self._set

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not self._header:
            if value[:2] == "A ":
                self.header = re.findall(r"[^\s]+", value[3:].strip())
            else:
                raise DataBlockException("Supported header start with '~A '")

    def parse(self, line):
        record = re.findall("\d+\.{0,1}(?=\d+)\d*", line.strip())
        if record:
            self._set.append( record )
