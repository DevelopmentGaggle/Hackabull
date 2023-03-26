import speechToText_engine
import sys
import time
import ChatGPT
import queue
import os
from io import BytesIO
from gtts import gTTS
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play


RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

#def startAudio(response_q, time_marker, mute_request):
transcription_q = queue.Queue()
thread = speechToText_engine.SpeechToText(transcription_q)
thread.start()

while 1:
    message = transcription_q.get()
    if message[1] == 1:
        sys.stdout.write(GREEN)
        sys.stdout.write("\r" + message[0] + "\n")
    else:
        sys.stdout.write(RED)
        sys.stdout.write("\r" + message[0])

    #while True:



# rbq = RankByQualifier("Strong problem-solving and analytical skills")
# rbq = RankByQualifier("motivated")
# rbq = RankByQualifier("confident and commanding")
#rbq = RankByQualifier("positive")
#print("Bad: " + rbq.get_prompt("I was unfortunately unable to meet the deadline. My VHDL code also never worked."))
#print("Good: " + rbq.get_prompt("I was unfortunately unable to meet the deadline. Despite this, I worked with my managers to develop a plan to recover from this and was able to meet the second milestone in advance of the deadline!"))


#chat_gpt3 = ChatGPT3(initial_context="""You are a senior computer engineer interviewing me for a position at your company, Google. You will ask several questions and I will respond to those questions until you initiate the end of the interview after four or so questions. The only exception to this will be during the intrpductions at the start of the mock interview where I introduce myself first

#""")

#for i in range(6):
#    user_input = input()
#    if user_input == "quit":
#        break
#    print(chat_gpt3.get_prompt(user_input, i > 3))

