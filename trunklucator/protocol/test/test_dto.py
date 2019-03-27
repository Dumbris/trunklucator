import pytest
import json
from unittest.mock import patch
import uuid

import trunklucator.const.msg as const_msg
import trunklucator.const.task_types as const_ttype
import trunklucator.protocol.dto as dto

def fake_uuid():
    return patch.object(uuid, 'uuid4', side_effect=['e5bfcc21-de44-47d9-9189-1f9f9145331f'])


MSG_TASK1 = '{"msg_id": null, "payload": {"meta": null, "task_id": "e5bfcc21-de44-47d9-9189-1f9f9145331f", "x": [[1, 2], [3, 4], [5, 6]]}, "reply_id": null, "type": "task"}'
MSG_LIST1 = '{"msg_id": "e5bfcc21-de44-47d9-9189-1f9f9145331f", "payload": null, "reply_id": null, "type": "list"}'


def test_message_task():
    X = [[1,2],[3,4],[5,6]]
    y = [0,1,0]
    label_name = ['Y', 'N']
    with fake_uuid():
        t = dto.Message(const_msg.TYPE_TASK, dto.Data(dto.get_id(), X, None))
    assert json.dumps(t.to_dict(), sort_keys=True) == MSG_TASK1
