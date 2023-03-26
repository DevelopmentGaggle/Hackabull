import ChatGPT
import queue
import sys
import speechToText_engine
import spotify_engine2
from spotify_engine2 import sp as sp
from threading import Thread
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


class DataDog:
    def __init__(self):
        self.chatGPT_enabled = True  # Set to false to disable chatGPT
        self.query = queue.Queue()
        self.stt_to_GUI = queue.Queue()
        self.response = queue.Queue()
        self.chatGPT_to_GUI = queue.Queue()
        self.is_talking = False
        self.ai = ChatGPT.VoiceAssistant()
        self.kill_threads = False
        self.canned_response_seed = 6
        self.canned_responses = ['Done!', 'Okay!', 'Sure, no problem!', 'Got it!', 'On it!', 'Alright!', 'Finished!']
    def stt_driver(self):
        thread = speechToText_engine.SpeechToText(self.query)
        thread.start()

        while not self.kill_threads:
            query = self.query.get()
            wakeWordPos = query[0].lower().find('sophie')
            if wakeWordPos >= 0:
                if query[1] == 1:
                    sys.stdout.write(GREEN)
                    sys.stdout.write("\r" + query[0] + "\n")
                    self.stt_to_GUI.put(query)

                    if self.chatGPT_enabled:
                        gpt_thread = Thread(target=self.ai.get_response, args=(query[0], self.response))
                        gpt_thread.start()
                    else:
                        self.response.put(['chatGPT is disabled, to enable set the data dog flag', 0])

                    while self.response.empty():
                        speechToText_engine.isPaused = True
                        pass

                    speechToText_engine.isPaused = False
                    response = self.response.get()
                    tts = response[0]
                    if response[1]:
                        self.chatGPT_to_GUI.put(response[0])
                        try:
                            exec(response[0])
                            print(response[0])
                            tts = self.canned_responses[(self.canned_response_seed * 3) % len(self.canned_responses)]
                            self.canned_response_seed *= 3
                            self.canned_response_seed += 1
                        except:
                            tts = 'Sorry, something went wrong'
                    else:
                        self.chatGPT_to_GUI.put(response[0])
                        # Straight up output!

                    mp3_fp = BytesIO()
                    tts = gTTS(text=tts, lang='en')
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)
                    song = AudioSegment.from_file(mp3_fp, format="mp3")

                    tts_thread = Thread(target=play, args=(song,))
                    tts_thread.start()
                    tts_thread.join()
                else:
                    sys.stdout.write(RED)
                    sys.stdout.write("\r" + query[0])
                    self.stt_to_GUI.put(query)





        # Do something to kill the other threads

    def run_stt(self):
        stt_thread = Thread(target=self.stt_driver)
        stt_thread.start()




