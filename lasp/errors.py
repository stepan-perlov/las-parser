class LasFormatException(Exception):
    pass

class VersionBlockException(LasFormatException):
    pass

class WellBlockException(LasFormatException):
    pass

class CurveBlockException(LasFormatException):
    pass

class ParameterBlockException(LasFormatException):
    pass

class OtherBlockException(LasFormatException):
    pass

class DataBlockException(LasFormatException):
    pass