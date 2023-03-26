import ChatGPT
import queue


class DataDog:
    def __init__(self):
        self.response_q = queue.Queue()
        self.is_talking = False

    def stt_driver(self):
        self.response_q = 0  # Example


