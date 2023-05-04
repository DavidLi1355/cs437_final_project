from tkinter import *
from src.time_display import TimeDisplay
from src.alarm import Alarm

root = Tk()
root.geometry("700x900")
root.resizable(0, 0)
root.title("Clock")


time_display = TimeDisplay(root)
time_display.get_time()

alarm = Alarm(root)
# alarm.play()

mainloop()
