import intlabeler.const.payload as payload
import intlabeler.const.msg as const_msg
from intlabeler.base.dto import AsDict
from collections import namedtuple
import json

MSG_VERSION_VAL = '1.0'

class Version():
    version = MSG_VERSION_VAL

class Data(namedtuple("Data", [ payload.X, 
                                payload.LABEL_NAME, 
                                payload.TITLE, 
                                payload.LABEL_TYPE,
                                payload.Y, 
                              ]), AsDict):
    pass



class ServerMsg(namedtuple("ServerMsg", [const_msg.DATA, const_msg.TYPE, const_msg.ID]), AsDict, Version):
    pass

