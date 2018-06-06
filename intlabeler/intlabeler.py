"""Interactive Labeler

This module includes an InteractiveLabeler.
"""

import asyncio, signal
from intlabeler.webserver.server import WebServer
from intlabeler.webserver.aiothread import AioThread

import intlabeler.protocol.dto as dto
import intlabeler.const.msg as const_msg
import intlabeler.const.task_types as const_ttype


TIMEOUT = 9000 #Do we really need it?

def signal_handler(loop):
    loop.remove_signal_handler(signal.SIGTERM)
    #is_working = False

class InteractiveLabeler:

    """Interactive Labeler

    InteractiveLabeler is a Labeler object that shows the feature through image
    using matplotlib and lets human label each feature through command line
    interface.

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

    def __enter__(self):
        self.start_thread()
        return self

    def __exit__(self, *args):
        self.stop_thread()
        return False


    def ask(self, X, label_name, title, task_type, y):
        #create task object
        task_data = dto.Data(dto.get_id(), X, label_name, title, task_type, y)
        coro = self.aiothread.server.add_task(task_data)
        future = self.aiothread.add_task(coro)
        #Make sure you wait for loop to start. Calling future.cancel() in main thread will cancel asyncio coroutine in background thread.
        try:
            result = future.result(TIMEOUT)
            return result.y
        except asyncio.TimeoutError:
            print('The coroutine took too long, cancelling the task')
            future.cancel()
        except Exception as exc:
            print('The coroutine raised an exception: {!r}'.format(exc))
        