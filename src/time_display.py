from tkinter import *
from enum import Enum
from time import strftime
from tkinter import Tk


class Time_Format(Enum):
    Military_Time = "Military Time"
    Standard_Time = "Standard Time"
    Analog_Time = "Analog Time"


class TimeDisplay:
    def __init__(self, root: Tk) -> None:
        self.current_format = Time_Format.Military_Time

        self.time_element: Label = Label(root, font=(
            'calibri', 40, 'bold'), foreground='black')
        self.time_element.place(relx=0.5, rely=0.5, anchor=CENTER)

        # drop down menu
        self.clicked = StringVar()
        self.clicked.set(self.current_format.value)
        options = [f.value for f in Time_Format]
        self.menu = OptionMenu(
            root, self.clicked,  *options)
        self.menu.pack()

    def get_time(self):
        self.current_format = Time_Format(self.clicked.get())

        if self.current_format == Time_Format.Military_Time:
            string = strftime('%H:%M:%S')
        elif self.current_format == Time_Format.Standard_Time:
            string = strftime('%I:%M:%S %p')
        else:
            string = "Analog"

        self.time_element.config(text=string)
        self.time_element.after(1, self.get_time)
