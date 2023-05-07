from tkinter import Tk, mainloop
from src.time_display import TimeDisplay
from src.alarm import Alarm
from src.speech_to_text import SpeechToText
from src.news import News
from src.music import Music

import threading
from server import run_server


# setup root
root = Tk()
root.geometry("700x900")
root.resizable(False, False)
root.title("Clock")


if __name__ == "__main__":
    # setup root
    root = Tk()
    root.geometry("700x900")
    root.resizable(False, False)
    root.title("Clock")

    # setup clock and alarm
    time_display = TimeDisplay(root, is_client=False)
    time_display.get_time()
    alarm = Alarm(root, is_client=False)
    # setup news and music
    news = News(root)
    music = Music(root)
    # setup text to speech control
    speech_to_text = SpeechToText(alarm, music)

    my_thread = threading.Thread(
        target=run_server,
        args=(
            time_display,
            alarm,
        ),
    )
    my_thread.start()

    mainloop()
    # Wait for the thread to complete
    my_thread.join()

    # clean up thread
    del alarm
    del news
time_display = TimeDisplay(root, is_client=False)
time_display.get_time()
alarm = Alarm(root, is_client=False)
news = News(root)
music = Music(root)
speech_to_text = SpeechToText(alarm, news, music)

my_thread = threading.Thread(
    target=run_server,
    args=(
        time_display,
        alarm,
    ),
)
my_thread.start()


mainloop()
print("Hi")
# Wait for the thread to complete
my_thread.join()
# clean up thread
del alarm
