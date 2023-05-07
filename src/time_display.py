from tkinter import Tk, Label, Canvas, StringVar, OptionMenu, CENTER
from enum import Enum
import time
import math
import socket


class TimeFormat(Enum):
    Military_Time = "Military Time"
    Standard_Time = "Standard Time"
    Analog_Time = "Analog Time"


class TimeColor(Enum):
    Black = "black"
    Red = "red"
    Green = "green"
    Blue = "blue"
    Yellow = "yellow"


class TimeDisplay:
    REL_Y = 0.4
    ANALOG_WIDTH = 400
    ANALOG_HEIGHT = 400

    def __init__(self, root: Tk, is_client: bool) -> None:
        self.current_format = TimeFormat.Military_Time
        self.current_color = TimeColor.Black
        self.is_client = is_client
        self.socket = None


        # if self.is_client:
        #     HOST = 'localhost'  # The server's hostname or IP address
        #     PORT = 5000  # The port used by the server
        #     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     self.socket.connect((HOST, PORT))


        # digital
        self.time_label: Label = Label(
            root, font=("calibri", 80, "bold"), foreground="black"
        )
        self.time_label.place(relx=0.5, rely=TimeDisplay.REL_Y, anchor=CENTER)
        # analog
        self.time_canvas = Canvas(
            root,
            width=TimeDisplay.ANALOG_WIDTH,
            height=TimeDisplay.ANALOG_HEIGHT,
        )
        self.time_canvas.place_forget()

        # drop down menu for format
        self.selected_format = StringVar()
        self.selected_format.set(self.current_format.value)
        options = [f.value for f in TimeFormat]
        self.menu_format = OptionMenu(root, self.selected_format, *options)
        self.menu_format.place(relx=0.4, rely=0.05, anchor=CENTER)

        # drop down menu for color
        self.selected_color = StringVar()
        self.selected_color.set(self.current_color.name)
        options = [f.name for f in TimeColor]
        self.menu_color = OptionMenu(root, self.selected_color, *options)
        self.menu_color.place(relx=0.6, rely=0.05, anchor=CENTER)

    def get_time(self):
        self.current_format = TimeFormat(self.selected_format.get())
        self.current_color = TimeColor[self.selected_color.get()]
        #
        if self.is_client and self.socket:
            message = 'FORMAT ' + self.current_format.value + '\n'
            self.socket.sendall(message.encode())
            message = 'COLOR ' + self.current_color.name + '\n'
            self.socket.sendall(message.encode())


        if (
            self.current_format == TimeFormat.Military_Time
            or self.current_format == TimeFormat.Standard_Time
        ):
            self.time_canvas.place_forget()
            self.time_label.place(
                relx=0.5, rely=TimeDisplay.REL_Y, anchor=CENTER
            )
            if self.current_format == TimeFormat.Military_Time:
                string = time.strftime("%H:%M:%S")
            else:
                string = time.strftime("%I:%M:%S %p")
            self.time_label.config(
                text=string, foreground=self.current_color.value
            )
        else:
            self.time_label.place_forget()
            self.time_canvas.place(
                relx=0.5, rely=TimeDisplay.REL_Y, anchor=CENTER
            )
            self.update_analog_clock()

        self.time_label.after(100, self.get_time)

    def update_analog_clock(self):
        self.time_canvas.delete("all")
        now = time.localtime()
        hour = now.tm_hour % 12
        minute = now.tm_min
        second = now.tm_sec

        # Draw clock face
        self.time_canvas.create_oval(
            6,
            6,
            TimeDisplay.ANALOG_WIDTH,
            TimeDisplay.ANALOG_HEIGHT,
            outline="black",
            width=2,
        )

        # Draw hour numbers
        for i in range(12):
            angle = i * math.pi / 6 - math.pi / 2
            x = (
                TimeDisplay.ANALOG_WIDTH / 2
                + 0.7 * TimeDisplay.ANALOG_WIDTH / 2 * math.cos(angle)
            )
            y = (
                TimeDisplay.ANALOG_HEIGHT / 2
                + 0.7 * TimeDisplay.ANALOG_WIDTH / 2 * math.sin(angle)
            )
            if i == 0:
                self.time_canvas.create_text(
                    x, y - 10, text=str(i + 12), font=("Helvetica", 12)
                )
            else:
                self.time_canvas.create_text(
                    x, y, text=str(i), font=("Helvetica", 12)
                )

        # Draw minute lines
        for i in range(60):
            angle = i * math.pi / 30 - math.pi / 2
            x1 = (
                TimeDisplay.ANALOG_WIDTH / 2
                + 0.8 * TimeDisplay.ANALOG_WIDTH / 2 * math.cos(angle)
            )
            y1 = (
                TimeDisplay.ANALOG_HEIGHT / 2
                + 0.8 * TimeDisplay.ANALOG_HEIGHT / 2 * math.sin(angle)
            )
            x2 = (
                TimeDisplay.ANALOG_WIDTH / 2
                + 0.9 * TimeDisplay.ANALOG_WIDTH / 2 * math.cos(angle)
            )
            y2 = (
                TimeDisplay.ANALOG_HEIGHT / 2
                + 0.9 * TimeDisplay.ANALOG_HEIGHT / 2 * math.sin(angle)
            )
            if i % 5 == 0:
                self.time_canvas.create_line(
                    x1, y1, x2, y2, fill="black", width=3
                )
            else:
                self.time_canvas.create_line(
                    x1, y1, x2, y2, fill="black", width=1
                )

        # Draw hour hand
        hour_angle = (hour + minute / 60) * math.pi / 6 - math.pi / 2
        hour_x = (
            TimeDisplay.ANALOG_WIDTH / 2
            + 0.5 * TimeDisplay.ANALOG_WIDTH / 2 * math.cos(hour_angle)
        )
        hour_y = (
            TimeDisplay.ANALOG_HEIGHT / 2
            + 0.5 * TimeDisplay.ANALOG_HEIGHT / 2 * math.sin(hour_angle)
        )
        self.time_canvas.create_line(
            TimeDisplay.ANALOG_WIDTH / 2,
            TimeDisplay.ANALOG_HEIGHT / 2,
            hour_x,
            hour_y,
            fill="black",
            width=6,
        )

        # Draw minute hand
        minute_angle = (minute + second / 60) * math.pi / 30 - math.pi / 2
        minute_x = (
            TimeDisplay.ANALOG_WIDTH / 2
            + 0.7 * TimeDisplay.ANALOG_WIDTH / 2 * math.cos(minute_angle)
        )
        minute_y = (
            TimeDisplay.ANALOG_HEIGHT / 2
            + 0.7 * TimeDisplay.ANALOG_HEIGHT / 2 * math.sin(minute_angle)
        )
        self.time_canvas.create_line(
            TimeDisplay.ANALOG_WIDTH / 2,
            TimeDisplay.ANALOG_HEIGHT / 2,
            minute_x,
            minute_y,
            fill="black",
            width=4,
        )

        # Draw second hand
        second_angle = second * math.pi / 30 - math.pi / 2
        second_x = (
            TimeDisplay.ANALOG_WIDTH / 2
            + 0.6 * TimeDisplay.ANALOG_WIDTH / 2 * math.cos(second_angle)
        )
        second_y = (
            TimeDisplay.ANALOG_HEIGHT / 2
            + 0.6 * TimeDisplay.ANALOG_WIDTH / 2 * math.sin(second_angle)
        )
        self.time_canvas.create_line(
            TimeDisplay.ANALOG_WIDTH / 2,
            TimeDisplay.ANALOG_HEIGHT / 2,
            second_x,
            second_y,
            fill="red",
            width=2,
        )

    def set_socket(self, socket):
        self.socket = socket
