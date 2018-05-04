import pytest
import json
import numpy as np
from unittest.mock import patch
import uuid

import intlabeler.const.msg as const_msg
import intlabeler.protocol.create as create

def uuid_prefix(prefix: str):
    return patch.object(uuid, 'uuid4', side_effect=['e5bfcc21-de44-47d9-9189-1f9f9145331f'])

def test_message_task():
    #X = np.random.rand(3,2)
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    with uuid_prefix('obj_a'):
        t = create.message(X, label_name, msg_type=const_msg.TYPE_TASK)
    #t2 = json.dumps(t.to_dict())
    #print(t2)
    assert json.dumps(t.to_dict()) == '{"data": {"x": [[1, 2], [3, 4], [5, 6]], "label_name": ["Y", "N"], "title": "", "label_type": "binary", "y": null}, "type": "task", "id": "e5bfcc21-de44-47d9-9189-1f9f9145331f"}'
