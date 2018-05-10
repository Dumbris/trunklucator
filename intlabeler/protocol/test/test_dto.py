import pytest
import json
import numpy as np
from unittest.mock import patch
import uuid

import intlabeler.const.msg as const_msg
import intlabeler.protocol.create as create

def uuid_prefix(prefix: str):
    return patch.object(uuid, 'uuid4', side_effect=['e5bfcc21-de44-47d9-9189-1f9f9145331f'])


MSG_TASK1 = '{"data": {"label_name": ["Y", "N"], "label_type": "binary", "title": "", "x": [[1, 2], [3, 4], [5, 6]], "y": null}, "id": "e5bfcc21-de44-47d9-9189-1f9f9145331f", "type": "task"}'
MSG_LIST1 = '{"id": "e5bfcc21-de44-47d9-9189-1f9f9145331f", "type": "list"}'

def test_message_task():
    #X = np.random.rand(3,2)
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    with uuid_prefix('obj_a'):
        t = create.server_msg(X, label_name, msg_type=const_msg.TYPE_TASK)
    assert json.dumps(t.to_dict(), sort_keys=True) == MSG_TASK1

def test_message_list():
    with uuid_prefix('obj_a'):
        t = create.client_req(msg_type=const_msg.TYPE_LIST)
    assert json.dumps(t.to_dict(), sort_keys=True) == MSG_LIST1