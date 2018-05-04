import intlabeler.const.task_types as task_types
import intlabeler.const.msg as const_msg
from intlabeler.protocol.dto import Data
import uuid
from typing import List
from intlabeler.protocol.dto import ServerMsg


def get_id():
    return str(uuid.uuid4())

def data(X, label_name: List[str], title: str = '', label_type:str = task_types.BINARY, y = None):
    if y:
        assert X.shape[0] == y.shape[0]
    return Data(X, label_name, title, label_type, y)        

def message(*args, **kwargs):
    msg_type = kwargs.pop("msg_type", const_msg.TYPE_TASK)
    d = data(*args, **kwargs)
    return ServerMsg(d, msg_type, get_id())
