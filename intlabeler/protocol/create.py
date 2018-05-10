import intlabeler.const.task_types as task_types
import intlabeler.const.msg as const_msg
from intlabeler.protocol.dto import Data, Error
import uuid
from typing import List
from intlabeler.protocol.dto import ServerMsg, ServerReq, ClientMsg, ClientReq, ServerError


def get_id():
    return str(uuid.uuid4())

def data(X, label_name: List[str], title: str = '', label_type:str = task_types.BINARY, y = None):
    if y:
        assert X.shape[0] == y.shape[0]
    return Data(X, label_name, title, label_type, y)        

def error(title: str, description: str = ''):
    return Error(title, description)        
    
def server_error(*args, **kwargs):
    """Parameters
       -------------
       title        : string error title
       description  : full text description
    """
    d = error(*args, **kwargs)
    return ServerError(d, const_msg.TYPE_ERROR, get_id())

def server_req(*args, **kwargs):
    msg_type = kwargs.pop("msg_type", const_msg.TYPE_TASK)
    return ServerReq(msg_type, get_id())

def server_msg(*args, **kwargs):
    msg_type = kwargs.pop("msg_type", const_msg.TYPE_TASK)
    d = data(*args, **kwargs)
    return ServerMsg(d, msg_type, get_id())

def message(*args, **kwargs):
    return server_msg(*args, **kwargs)


#Client side requests    
def client_req(*args, **kwargs):
    msg_type = kwargs.pop("msg_type", const_msg.TYPE_LIST)
    return ClientReq(msg_type, get_id())

def client_msg(*args, **kwargs):
    msg_type = kwargs.pop("msg_type", None)
    d = data(*args, **kwargs)
    return ClientMsg(d, msg_type, get_id())