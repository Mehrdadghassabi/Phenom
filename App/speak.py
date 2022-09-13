import pyttsx3
from langdetect import detect
import sys

phenom_speech, language_mode = sys.argv[1], sys.argv[2]

engine = pyttsx3.init()
if language_mode=='persian':
    engine.setProperty('voice','persian')
elif language_mode == None or language_mode == "none" or language_mode == "None":
    engine.say("not response")
    engine.runAndWait()
    exit()
elif detect(phenom_speech)=='en':
    engine.setProperty('voice','english')
engine.say(phenom_speech)
engine.runAndWait()