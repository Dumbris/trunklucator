import const
from collections import namedtuple
import json

MSG_VERSION_VAL = '1.0'

class Base(object):
    def __init__(self, type_, version):
        self.type = type_
        self.version = version

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class ServerTask(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(const.MSG_TYPE_TASK, MSG_VERSION_VAL)
