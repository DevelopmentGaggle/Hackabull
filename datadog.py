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
        self.stt_to_GUI = queue.Queue()
        self.response = queue.Queue()
        self.chatGPT_to_GUI = queue.Queue()
        self.is_talking = False
        self.ai = ChatGPT.VoiceAssistant()

    def stt_driver(self):
        thread = speechToText_engine.SpeechToText(self.query)
        thread.start()

        while 1:
            query = self.query.get()
            if query[1] == 1:
                sys.stdout.write(GREEN)
                sys.stdout.write("\r" + query[0] + "\n")

                gpt_thread = Thread(target=self.ai.get_response, args=(query[0], self.response))
                gpt_thread.start()
            else:
                sys.stdout.write(RED)
                sys.stdout.write("\r" + query[0])

            self.stt_to_GUI.put(query)

            if self.response.empty():
                pass
            else:
                response = self.response.get()
                self.chatGPT_to_GUI.put(response[0])




    def run_stt(self):
        stt_thread = Thread(target=self.stt_driver)
        stt_thread.start()




