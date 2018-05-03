import intlabeler.const as const
from intlabeler.dto_base import AsDict
from collections import namedtuple
import json

MSG_VERSION_VAL = '1.0'

class Version():
    version = MSG_VERSION_VAL

class Data(namedtuple("Data", [ const.MSG_DATA_X, 
                                const.MSG_DATA_LABEL_NAME, 
                                const.MSG_DATA_TITLE, 
                                const.MSG_DATA_LABEL_TYPE,
                                const.MSG_DATA_Y, 
                              ]), AsDict):
    pass



class ServerMsg(namedtuple("ServerMsg", [const.MSG_DATA, const.MSG_TYPE, const.MSG_ID]), AsDict, Version):
    pass

