from tkinter import *
from tkinter.ttk import *
from src.time_display import TimeDisplay

root = Tk()
root.geometry("700x700")
root.resizable(0, 0)
root.title("Clock")


time_display = TimeDisplay(root)
time_display.get_time()


mainloop()
