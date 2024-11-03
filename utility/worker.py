import asyncio
from PyQt6.QtCore import QThread, pyqtSignal

class AsyncWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.func(*self.args, **self.kwargs))
        self.finished.emit(*result)
