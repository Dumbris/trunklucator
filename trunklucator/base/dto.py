from collections import OrderedDict

from datetime import datetime


def namedtuple_asdict(obj):
    if hasattr(obj, "_asdict"): # detect namedtuple
        return OrderedDict(zip(obj._fields, (namedtuple_asdict(item) for item in obj)))
    elif isinstance(obj, str): # iterables - strings
        return obj
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "keys"): # iterables - mapping
        return OrderedDict(zip(obj.keys(), (namedtuple_asdict(item) for item in obj.values())))
    elif hasattr(obj, "__iter__"): # iterables - sequence
        return type(obj)((namedtuple_asdict(item) for item in obj))
    else: # non-iterable cannot contain namedtuples
        return obj


class AsDict():
    def to_dict(self):
        return namedtuple_asdict(self)
