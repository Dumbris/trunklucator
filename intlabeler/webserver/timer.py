from time import sleep, time

class Timed():
    """A simple "timer" context manager. It prints execution time."""

    def __enter__(self):
        self.start = time()
        print("Starting at {}".format(self.start))
        return self

    def __exit__(self, type, value, traceback):
        # This code is guaranteed to run
        if traceback:
            print("type: {}".format(type))
            print("value: {}".format(value))
            print("traceback: {}".format(traceback))

        self.end = time()
        total = self.end - self.start
        print("Ending at {} (total: {})".format(self.end, total))
