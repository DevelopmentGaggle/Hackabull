import ChatGPT
import queue
import sys
import speechToText_engine
from threading import Thread

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

class DataDog:
    def __init__(self):
        self.query = queue.Queue()
        self.stt_to_chatGPT = queue.Queue()
        self.stt_to_GUI = queue.Queue()
        self.is_talking = False

    def stt_driver(self):
        thread = speechToText_engine.SpeechToText(self.query)
        thread.start()

        while 1:
            message = self.query.get()
            if message[1] == 1:
                sys.stdout.write(GREEN)
                sys.stdout.write("\r" + message[0] + "\n")
                self.stt_to_chatGPT.put(message[0])
            else:
                sys.stdout.write(RED)
                sys.stdout.write("\r" + message[0])

            self.stt_to_GUI.put([message[0], message[1]])

    def run_stt(self):
        stt_thread = Thread(target=self.stt_driver)
        stt_thread.start()



