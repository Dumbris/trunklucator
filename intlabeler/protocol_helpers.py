import intlabeler.const as const
from intlabeler.protocol import Data
import uuid
from typing import List


def get_id():
    return str(uuid.uuid4())

def create_data(X, label_name: List[str], title: str = '', label_type:str = const.LABEL_TYPE_BINARY, y = None):    
        if y:
            assert X.shape[0] == y.shape[0]
        return Data(X, label_name, title, label_type, y)        