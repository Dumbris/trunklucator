"""Web UI

This module includes an WebUI.
"""

import asyncio, signal
from trunklucator.webserver.server import WebServer
from trunklucator.webserver.aiothread import AioThread

import trunklucator.protocol.dto as dto
import trunklucator.const.msg as const_msg
import trunklucator.const.task_types as const_ttype

from typing import List

def signal_handler(loop):
    loop.remove_signal_handler(signal.SIGTERM)
    #is_working = False

class BaseUI:

    """Base class for UI

    Parameters
    ----------
    label_name: list
        Let the label space be from 0 to len(label_name)-1, this list
        corresponds to each label's name.

    """

    def __init__(self, *args, **kwargs):
        self.aiothread = None
        self.loop = None
        self.ws = None
        self.args = args
        self.kwargs = kwargs

    def start_thread(self):
        self.aiothread = AioThread()
        self.loop = self.aiothread.get_loop()
        #self.loop.add_signal_handler(signal.SIGTERM, signal_handler, self.loop)
        self.ws = WebServer(loop=self.loop, *self.args, **self.kwargs)
        self.aiothread.set_server(self.ws)
        self.aiothread.start()
        self.aiothread.event.wait()

    def stop_thread(self):
        self.aiothread.finalize()

    def open(self):
        self.start_thread()
        return self

    def close(self, *args):
        self.stop_thread()
        return False

    def __enter__(self):
        self.start_thread()
        return self

    def __exit__(self, *args):
        self.stop_thread()
        return False

    def ask(self, X, meta=None, default=-1):
        return default

    def update(self, X):
        return None



class WebUI(BaseUI):
    task_counter:int = 1
    """TODO!

    InteractiveLabeler is a Labeler object that shows the feature through html
    using javascript and lets human label each feature.

    Parameters
    ----------
    label_name: list
        Let the label space be from 0 to len(label_name)-1, this list
        corresponds to each label's name.

    """
    #def __init__(self, *args, **kwargs):
    #    super(WebUI, self).__init__(*args, **kwargs)

    def ask(self, X, meta=None, default=-1):
        #create task object
        task_data = dto.Data(self.task_counter, X, meta)
        self.task_counter += 1
        coro = self.aiothread.server.add_task(task_data)
        future = self.aiothread.add_task(coro)
        #Make sure you wait for loop to start. Calling future.cancel() in main thread will cancel asyncio coroutine in background thread.
        try:
            result = future.result()
            return result
        except asyncio.TimeoutError:
            print('The coroutine took too long, cancelling the task')
            future.cancel()
        except Exception as exc:
            print('The coroutine raised an exception: {!r}'.format(exc))
        return default


    def update(self, X):
        #create task object
        coro = self.aiothread.server.publish_update(dto.Update(X))
        _ = self.aiothread.add_task(coro)