import sys
import traceback

from PySide2.QtCore import QRunnable, QObject, Signal


class Worker(QRunnable):
    """ The Worker class aims to add concurrency throughout the
    ZOIA Librarian by delegating tasks to different threads. This
    ensures that the application can run smoothly.
    """

    def __init__(self, fn, *args, **kwargs):
        """ Initializes the class with the required parameters.

        fn: The function the Worker thread will target.
        args: The arguments passed that are required to execute fn.
        kwargs: Any additional key word arguments the thread requires.
        """

        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    def run(self):
        """ Override the default run method to force workers to execute
        the passed function during their initialization.
        """

        try:
            result = self.fn(*self.args, **self.kwargs)
        except InterruptedError:
            traceback.print_exc()
            exc_type, value = sys.exc_info()[:2]
            self.signals.error.emit((exc_type, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class WorkerSignals(QObject):
    """ The WorkerSignals class (enum) is responsible for defining
    signals to be used for communication with the UI by the Workers.
    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
