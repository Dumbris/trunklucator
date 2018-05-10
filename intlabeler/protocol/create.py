import intlabeler.const.task_types as task_types
import intlabeler.const.msg as const_msg
from intlabeler.protocol.dto import Data, Error
import uuid
from typing import List
from intlabeler.protocol.dto import Message


def get_id():
    return str(uuid.uuid4())