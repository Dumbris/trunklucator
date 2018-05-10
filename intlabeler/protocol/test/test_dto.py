import pytest
import json
import numpy as np
from unittest.mock import patch
import uuid

import intlabeler.const.msg as const_msg
import intlabeler.const.task_types as const_ttype
import intlabeler.protocol.dto as dto

def uuid_prefix(prefix: str):
    return patch.object(uuid, 'uuid4', side_effect=['e5bfcc21-de44-47d9-9189-1f9f9145331f'])


MSG_TASK1 = '{"msg_id": null, "payload": {"label_name": ["Y", "N"], "label_type": "binary", "task_id": "e5bfcc21-de44-47d9-9189-1f9f9145331f", "title": "Test data 1", "x": [[1, 2], [3, 4], [5, 6]], "y": [0, 1, 0]}, "reply_id": null, "type": "task"}'
MSG_LIST1 = '{"msg_id": "e5bfcc21-de44-47d9-9189-1f9f9145331f", "payload": null, "reply_id": null, "type": "list"}'

def test_message_task():
    #X = np.random.rand(3,2)
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    with uuid_prefix('obj_a'):
        t = dto.Message(const_msg.TYPE_TASK, dto.Data(dto.get_id(), X, label_name, "Test data 1", const_ttype.BINARY, y))
    assert json.dumps(t.to_dict(), sort_keys=True) == MSG_TASK1

def test_message_list():
    with uuid_prefix('obj_a'):
        t = dto.Message(const_msg.TYPE_LIST, msg_id=dto.get_id())
    assert json.dumps(t.to_dict(), sort_keys=True) == MSG_LIST1