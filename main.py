from tkinter import Tk, mainloop
from src.time_display import TimeDisplay
from src.alarm import Alarm
from src.speech_to_text import SpeechToText
from src.news import News

# setup root
root = Tk()
root.geometry("700x900")
root.resizable(False, False)
root.title("Clock")

# setup clock and alarm
time_display = TimeDisplay(root)
time_display.get_time()
alarm = Alarm(root)

speech_to_text = SpeechToText()
news = News(root)

mainloop()
print("Hi")
# clean up thread
del alarm
