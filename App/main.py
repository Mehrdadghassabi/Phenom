import time
import argparse
from programy.clients.embed.configfile import EmbeddedConfigFileBot

mode = "text"
voice = "pyttsx3"
terminate = ['bye', 'buy', 'shutdown', 'exit', 'quit', 'gotosleep', 'goodbye', 'خروج']
language_modes = ('en-US', 'fa-IR')
current_language_mode = 'en-US'
language_modes_commands = ['change language', 'change', 'تغییر زبان', 'تغییر']

def get_arguments():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('params')
    optional.add_argument('-v', '--voice', action='store_true', required=False,
                          help='Enable voice mode')
    optional.add_argument('-g', '--gtts', action='store_true', required=False,
                          help='Enable Google Text To Speech engine')
    arguments = parser.parse_args()
    return arguments


def gtts_speak(phenom_speech):
    tts = gTTS(text=phenom_speech, lang='en')
    tts.save('phenom_speech.mp3')
    mixer.init()
    mixer.music.load('phenom_speech.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def offline_speak(phenom_speech):
    engine = pyttsx3.init()
    if(lang=='persian'):
        engine.setProperty('voice','persian')
    engine.say(phenom_speech)
    engine.runAndWait()


def speak(phenom_speech):
    if voice == "gTTS":
        gtts_speak(phenom_speech)
    else:
        offline_speak(phenom_speech)


def listen(language_mode):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk to Phenom: ")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        response = r.recognize_google(audio, language=language_mode)
        print(response)
        return response
    except sr.UnknownValueError:
        speak(
            "I couldn't understand what you said! Would you like to repeat?")
        return(listen(current_language_mode))
    except sr.RequestError as e:
        print("Could not request results from " +
              "Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    args = get_arguments()

    if (args.voice):
        try:
            import speech_recognition as sr
            mode = "voice"
        except ImportError:
            print("\nInstall SpeechRecognition to use this feature." +
                  "\nStarting text mode\n")
    if (args.gtts):
        try:
            from gtts import gTTS
            from pygame import mixer
            voice = "gTTS"
        except ImportError:
            import pyttsx3
            print("\nInstall gTTS and pygame to use this feature." +
                  "\nUsing pyttsx\n")
    else:
        import pyttsx3

    my_bot = EmbeddedConfigFileBot('tmp.yaml', 'logging.yaml')
    client_context = my_bot.create_client_context('testuser')
    # bot now ready for use
    while True:
        client_context.bot.get_conversation(client_context).set_property("language", "english")
        if mode == "voice":
            response = listen(current_language_mode)
        else:
            response = input("talk to Phenom: ")
        if response.lower().replace(" ", "") in terminate:
            break
        if response.lower().strip() in language_modes_commands:
            current_language_mode = language_modes[1] if current_language_mode == language_modes[0] else language_modes[0]
            if current_language_mode == 'en-US':
                lang = 'english'
                speak("the language is changed")
            else:
                lang = 'persian'
                speak("زبان تغییر کرد")
            continue
        phenom_speech = my_bot.process_question(client_context, response)
        
        print("Phenom: " + phenom_speech)
        if not phenom_speech:
            lang = 'english'
            speak('not response')
            continue
        lang = client_context.bot.get_conversation(client_context).property("language")
        speak(phenom_speech)
