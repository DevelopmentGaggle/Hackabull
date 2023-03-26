import ChatGPT
import queue
from threading import Thread


class DataDog:
    def __init__(self):
        self.response = queue.Queue()
        self.is_talking = False

    def stt_driver(self):
        self.response = 0  # Example

    def run_tts(self):
        tts_thread = Thread(target=self.stt_driver)
        tts_thread.start()



