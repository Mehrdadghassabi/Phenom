import subprocess
import sys

import pyttsx3
import speech_recognition as sr
from langdetect import detect
from programy.clients.embed.configfile import EmbeddedConfigFileBot
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from gui.untitled2.Login_main_ui import login_window
from gui.untitled2.main_main_ui import main_window


class Controller():
    mode = "text"
    voice = "pyttsx3"
    terminate = ['bye', 'buy', 'shutdown', 'exit',
                 'quit', 'gotosleep', 'goodbye', 'خروج']
    language_modes = ('en-US', 'fa-IR')
    current_language_mode = 'en-US'
    language_modes_commands = [
        'change language', 'change', 'تغییر زبان', 'تغییر']
    def __init__(self):
        self.my_bot = EmbeddedConfigFileBot('tmp.yaml', 'logging.yaml')
        self.client_context = self.my_bot.create_client_context('testuser')

    def show_login(self):
        self.login = login_window()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.window = main_window()
        self.login.close()
        self.thread = recognition()
        self.thread.finished.connect(self.window.update_mic_send_button)
        self.thread.output["QString"].connect(self.response_by_voice_end)
        self.window.mic_button.clicked.connect(self.response_by_voice_start)
        self.speak_thread = speak()
        self.speak_thread.finished.connect(self.window.update_mic_send_button)
        self.window.send_button.clicked.connect(self.response_by_text_start)
        self.window.show()

    def offline_speak(self, phenom_speech, language_mode):
        engine = pyttsx3.init()
        if language_mode == 'persian':
            engine.setProperty('voice', 'persian')
        elif language_mode == None or language_mode == "none" or language_mode == "None":
            engine.say("not response")
            engine.runAndWait()
            return
        elif detect(phenom_speech) == 'en':
            engine.setProperty('voice', 'english')
        engine.say(phenom_speech)
        engine.runAndWait()

    def response_by_voice_start(self):
        self.window.mic_button.setEnabled(False)
        self.window.send_button.setEnabled(False)
        self.thread.render(self.current_language_mode)

    def response_by_voice_end(self, response):
        self.client_context.bot.get_conversation(self.client_context).set_property("language", "english")
        if response == "internet problem may be occured" or \
           response == "I couldn't understand what you said! Would you like to repeat?":
            self.offline_speak(response, None)
            return
        if response.lower().replace(" ", "") in self.terminate:
            self.window.close()
            return
        if response.lower().strip() in self.language_modes_commands:
            self.current_language_mode = self.language_modes[
                1] if self.current_language_mode == self.language_modes[0] else self.language_modes[0]
            if self.current_language_mode == 'en-US':
                self.speak_thread.render("english", "the language is changed")
            else:
                self.speak_thread.render("persian", "زبان تغییر کرد")
            return

        self.window.messageBox.addTextMsg(response, False)
        phenom_speech = self.my_bot.process_question(
            self.client_context, response)
        if response == "" or phenom_speech == "":
            self.window.messageBox.addTextMsg("not response", True)
            self.speak_thread.render("none", "not response")
            return
        lang = self.client_context.bot.get_conversation(
            self.client_context).property("language")
        self.window.messageBox.addTextMsg(phenom_speech, True)
        self.speak_thread.render(str(lang), phenom_speech)

    def response_by_text_start(self):
        self.window.mic_button.setEnabled(False)
        self.window.send_button.setEnabled(False)
        self.client_context.bot.get_conversation(self.client_context).set_property("language", "english")
        response = str(self.window.chat_le.text())
        if response.lower().replace(" ", "") in self.terminate:
            self.window.close()
            return
        if response.lower().strip() in self.language_modes_commands:
            self.current_language_mode = self.language_modes[
                1] if self.current_language_mode == self.language_modes[0] else self.language_modes[0]
            if self.current_language_mode == 'en-US':
                self.speak_thread.render("english", "the language is changed")
            else:
                self.speak_thread.render("persian", "زبان تغییر کرد")
            return
        self.window.messageBox.addTextMsg(response, False)
        phenom_speech = self.my_bot.process_question(
            self.client_context, response)
        if response == "" or phenom_speech == "":
            self.window.messageBox.addTextMsg("not response", True)
            self.speak_thread.render("none", "not response")
            return
        lang = self.client_context.bot.get_conversation(
            self.client_context).property("language")
        self.window.messageBox.addTextMsg(phenom_speech, True)
        self.speak_thread.render(str(lang), phenom_speech)



class recognition(QThread):
    output = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.lang = str()

    def render(self, lang):
        self.lang = lang
        self.start()

    def __del__(self):
        try:
            self.exiting = True
            self.wait()
        except:
            pass

    def run(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        if not self.exiting:
            try:
                response = r.recognize_google(audio, language=self.lang)
                print(response)
                self.output.emit(response)
            except sr.UnknownValueError:
                # self.offline_speak(
                #     "I couldn't understand what you said! Would you like to repeat?", "english")
                self.output.emit("I couldn't understand what you said! Would you like to repeat?")
                # return(self.voice_command(self.current_language_mode))
            except sr.RequestError as e:
                print("Could not request results from " +
                      "Google Speech Recognition service; {0}".format(e))
                self.output.emit("intenet problem may be occured")


class speak(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.lang = str()
        self.speaking_text = str()

    def render(self, lang, text):
        self.lang = lang
        self.speaking_text = text
        self.start()

    def __del__(self):
        try:
            self.exiting = True
            self.wait()
        except:
            pass

    def run(self):
        if not self.exiting:
            engine = pyttsx3.init()
            if self.lang == 'persian':
                engine.setProperty('voice', 'persian')
            elif self.lang == None or self.lang == "none" or self.lang == "None":
                engine.say("not response")
                engine.runAndWait()
                return
            elif self.lang == "english":
                engine.setProperty('voice', 'english')
            engine.say(self.speaking_text)
            engine.runAndWait()



def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
