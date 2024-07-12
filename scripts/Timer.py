from time import time


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.c = 0

    def start(self):
        self.start_time = time()
        self.c = 0

    def end(self):
        if not self.c:
            self.end_time = time()
            self.c = 1