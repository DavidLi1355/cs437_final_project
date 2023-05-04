import sys
from tkinter import Tk, mainloop
from src.time_display import TimeDisplay
from src.alarm import Alarm

# setup root
root = Tk()
root.geometry("700x900")
root.resizable(False, False)
root.title("Clock")

# setup clock and alarm
time_display = TimeDisplay(root)
time_display.get_time()
alarm = Alarm(root)

mainloop()

# clean up thread
del alarm

