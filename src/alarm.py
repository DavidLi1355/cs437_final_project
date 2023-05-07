import time
from tkinter import (
    Tk,
    Button,
    Entry,
    Label,
    CENTER,
)
from datetime import datetime
from threading import Thread, Lock, Event
from playsound import playsound
import socket

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

    def __init__(self, root: Tk, is_client: bool) -> None:
        self.root = root
        self.is_client = is_client
        self.socket = None

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

        self.event = Event()
        self.handler = Thread(
            target=AlarmHandler.handler, args=(self.alarm_time, self.event)
        )
        self.handler.start()

    def __del__(self):
        self.event.set()
        self.handler.join()

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
        # if instance is a client, post changes to server
        if self.is_client:
            message = 'SET_ALARM ' + self.hour_text.get() + ' ' + self.minute_text.get() + '\n'
            print(message)
            self.socket.sendall(message.encode())





    def set_alarm_from_speech(self, hour, minute):
        if hour >= 24 or minute >= 60:
            # handle error
            return
        with Alarm.alarm_time_lock:
            self.alarm_time.set_time(hour, minute)
            self.alarm_time.enable()

    def reset_alarm(self):
        with Alarm.alarm_time_lock:
            self.alarm_time.disable()
            if self.is_client:
                message = 'RESET_ALARM' + '\n'
                print(message)
                self.socket.sendall(message.encode())


    def set_socket(self, socket):
        self.socket = socket

class AlarmHandler:
    CHECK_INTERVAL_SEC = 5

    @staticmethod
    def handler(alarm_time: AlarmTime, event: Event):
        while True:
            if event.isSet():
                break

            if not alarm_time.on:
                AlarmHandler.sleep_sec()
                continue

            curr_time = datetime.now().strftime("%H : %M")
            if curr_time != str(alarm_time):
                AlarmHandler.sleep_sec()
                continue

            playsound("./resources/morning-clock-alarm.mp3", block=False)
            with Alarm.alarm_time_lock:
                alarm_time.disable()

    @staticmethod
    def sleep_sec():
        # sleep for CHECK_INTERVAL_SEC
        time.sleep(
            AlarmHandler.CHECK_INTERVAL_SEC
            - time.time() % AlarmHandler.CHECK_INTERVAL_SEC
        )
