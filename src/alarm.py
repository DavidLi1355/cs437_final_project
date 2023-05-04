import time
from tkinter import (
    Tk,
    Button,
    Text,
    Entry,
    Label,
    Canvas,
    StringVar,
    OptionMenu,
    CENTER,
)
from datetime import datetime
from threading import Thread, Lock
from playsound import playsound


class AlarmTime:
    def __init__(self, hour, minute, root) -> None:
        self.root = root
        self.hour = hour
        self.minute = minute
        self.on = False
        self.label = Label(root, text=str(self))
        self.label.place_forget()

    def set_time(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def enable(self):
        self.on = True
        self.label = Label(self.root, text=str(self))
        self.label.place(relx=0.5, rely=0.9, anchor=CENTER)

    def disable(self):
        self.on = False
        self.label.place_forget()

    def __str__(self) -> str:
        return str(self.hour).zfill(2) + " : " + str(self.minute).zfill(2)


class Alarm:
    alarm_time_lock = Lock()

    def __init__(self, root: Tk) -> None:
        self.root = root
        vcmd = root.register(self.is_num_callback)
        self.hour_text = Entry(
            root, validate="all", validatecommand=(vcmd, "%P"), width=2
        )
        self.hour_text.place(relx=0.45, rely=0.8, anchor=CENTER)
        Label(root, text=":").place(relx=0.5, rely=0.8, anchor=CENTER)
        self.minute_text = Entry(
            root, validate="all", validatecommand=(vcmd, "%P"), width=2
        )
        self.minute_text.place(relx=0.55, rely=0.8, anchor=CENTER)
        self.set_button = Button(
            root, text="Set Alarm", command=self.set_alarm
        )
        self.set_button.place(relx=0.4, rely=0.85, anchor=CENTER)
        self.reset_button = Button(
            root, text="Reset Alarm", command=self.reset_alarm
        )
        self.reset_button.place(relx=0.6, rely=0.85, anchor=CENTER)
        self.alarm_time = AlarmTime(0, 0, root)

        self.handler = Thread(
            target=AlarmHandler.handler, args=(self.alarm_time,)
        )
        self.handler.start()

    def is_num_callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def set_alarm(self):
        if self.hour_text.get() == "" or self.minute_text.get() == "":
            return
        hour = int(self.hour_text.get())
        minute = int(self.minute_text.get())
        if hour >= 24 or minute >= 60:
            # handle error
            return
        with Alarm.alarm_time_lock:
            self.alarm_time.set_time(hour, minute)
            self.alarm_time.enable()

    def reset_alarm(self):
        with Alarm.alarm_time_lock:
            self.alarm_time.disable()


class AlarmHandler:
    @staticmethod
    def handler(alarm_time: AlarmTime):
        while True:
            if not alarm_time.on:
                time.sleep(0.1)
                continue

            curr_time = datetime.now().strftime("%H : %M")
            if curr_time != str(alarm_time):
                time.sleep(0.1)
                continue

            playsound("./resources/morning-clock-alarm.mp3", block=False)
            with Alarm.alarm_time_lock:
                alarm_time.disable()
