# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import threading



class SpeechToTextHandler:
    @staticmethod
    def handler(recognizer):
        while (1):
            # Exception handling to handle
            # exceptions at the runtime
            try:
                # use the microphone as source for input.
                with sr.Microphone() as source2:
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    recognizer.adjust_for_ambient_noise(source2, duration=0.3)

                    # listens for the user's input
                    audio2 = recognizer.listen(source2)

                    # Using google to recognize audio
                    MyText = recognizer.recognize_google(audio2)
                    MyText = MyText.lower()
                    SpeechToTextHandler.ParseCommand(MyText)
                    # SpeakText(MyText)

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred")

    @staticmethod
    def ParseCommand(command):
        print("Did you say ", command)

        command_functions = {
            "set alarm": SpeechToTextHandler.set_alarm,
            "cancel alarm": SpeechToTextHandler.cancel_alarm,
            "snooze alarm": SpeechToTextHandler.snooze_alarm,
            "check time": SpeechToTextHandler.check_time,
            "set timer": SpeechToTextHandler.set_timer,
            "cancel timer": SpeechToTextHandler.cancel_timer,
            "turn off timer": SpeechToTextHandler.turn_off_timer,
            "play music": SpeechToTextHandler.play_music
        }

        words = command.split()

        # Get the first two words as a single string
        first_two_words = " ".join(words[:2])

        # Call the appropriate function based on the command
        if first_two_words in command_functions:
            command_functions[first_two_words]()
        else:
            print(f"The command '{command}' does not match any possible commands.")

        return

    @staticmethod
    def set_alarm():
        # words is formatted ['set', 'alarm', 'time']
        # if len(words) < 3:
        #     return "Error setting time"
        print("Setting alarm to time ")

    @staticmethod
    def cancel_alarm():
        print("Canceling alarm...")

    @staticmethod
    def snooze_alarm():
        print("Snoozing alarm...")

    @staticmethod
    def check_time():
        print("Checking time...")

    @staticmethod
    def set_timer():
        print("Setting timer...")

    @staticmethod
    def cancel_timer():
        print("Canceling timer...")

    @staticmethod
    def turn_off_timer():
        print("Turning off timer...")

    @staticmethod
    def play_music():
        print("Playing music...")


class SpeechToText:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.handler = threading.Thread(target=SpeechToTextHandler.handler, args=(self.recognizer,))
        self.handler.start()

