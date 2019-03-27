"""
trunklucator
======

Available subpackages
---------------------
base
    Defines interface and dataset object.

"""

__all__ = ["base", "const", "protocol", "webserver"]

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

# pylint: disable-msg=W0614,W0401,W0611,W0622

# flake8: noqa

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("aiohttp",)
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies


from trunklucator.trunklucator import *
