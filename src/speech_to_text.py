# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import threading
from src.alarm import Alarm
from threading import Thread, Lock, Event


class SpeechToTextHandler:
    @staticmethod
    def handler(recognizer: sr.Recognizer):
        while 1:
            print("in loop")
            try:
                with sr.Microphone() as source:
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    recognizer.adjust_for_ambient_noise(source)

                    audio = recognizer.listen(source)
                    my_text = recognizer.recognize_google(audio)
                    my_text = my_text.lower()
                    SpeechToTextHandler.ParseCommand(my_text)

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred")

    @staticmethod
    def ParseCommand(command):
        print("command", command)
        command_functions = {
            "set alarm": SpeechToTextHandler.set_alarm,
            "cancel alarm": SpeechToTextHandler.cancel_alarm,
            "play music": SpeechToTextHandler.play_music,
            "play news": SpeechToTextHandler.play_news,
        }

        words = command.split()

        # Get the first two words as a single string
        first_two_words = " ".join(words[:2])

        # Call the appropriate function based on the command
        if first_two_words in command_functions:
            command_functions[first_two_words](words)

    @staticmethod
    def set_alarm(words):
        if len(words) < 3:
            return

        hour = -1
        minute = 0
        is_pm = False

        if words[-1] == "p.m.":
            is_pm = True

        try:
            if ":" in words[2]:
                hour_and_minute = words[2].split(":")
                hour = int(hour_and_minute[0])
                minute = int(hour_and_minute[1])
            else:
                hour = int(words[2])
        except Exception:
            return

        if is_pm:
            hour += 12

        print("Setting alarm...", hour, minute)

        if hour == -1:
            return

        SpeechToText.alarm_obj.set_alarm_from_speech(hour, minute)

    @staticmethod
    def cancel_alarm(words):
        print("Canceling alarm...")
        SpeechToText.alarm_obj.reset_alarm()

    @staticmethod
    def play_music(words):
        print("Playing music...")

    @staticmethod
    def play_news(words):
        print("Playing news...")


class SpeechToText:
    alarm_obj: Alarm = None

    def __init__(self, alarm: Alarm) -> None:
        SpeechToText.alarm_obj = alarm

        self.recognizer = sr.Recognizer()
        self.handler = threading.Thread(
            target=SpeechToTextHandler.handler, args=(self.recognizer,)
        )
        self.handler.start()
        self.event = Event()

    def __del__(self) -> None:
        self.event.set()
        self.handler.join()
