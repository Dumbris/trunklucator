import pytest
import json
import numpy as np

import intlabeler.const as const
from intlabeler.protocol import ServerMsg, create_data, get_id

def test_channel():
    #X = np.random.rand(3,2)
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    d = create_data(X, label_name)
    t = ServerMsg(d, const.MSG_TYPE_TASK, get_id())
    t2 = json.dumps(t.to_dict())
    print(t2)
    #assert json.dumps(c.to_dict()) == '{"call_sign": "NBCSNHD", "count": 540}'
