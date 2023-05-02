from tkinter import *
from enum import Enum
from time import strftime
import time
import math

ANALOG_WIDTH = 400
ANALOG_HEIGHT = 400


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
    def __init__(self, root: Tk) -> None:
        self.current_format = TimeFormat.Military_Time
        self.current_color = TimeColor.Black

        # digital
        self.time_label: Label = Label(
            root, font=("calibri", 50, "bold"), foreground="black"
        )
        self.time_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # analog
        self.time_canvas = Canvas(
            root, width=ANALOG_WIDTH, height=ANALOG_HEIGHT, bg="white"
        )
        self.time_canvas.place_forget()

        # drop down menu for format
        self.selected_format = StringVar()
        self.selected_format.set(self.current_format.value)
        options = [f.value for f in TimeFormat]
        self.menu_format = OptionMenu(root, self.selected_format, *options)
        self.menu_format.pack()

        # drop down menu for color
        self.selected_color = StringVar()
        self.selected_color.set(self.current_color.name)
        options = [f.name for f in TimeColor]
        self.menu_color = OptionMenu(root, self.selected_color, *options)
        self.menu_color.pack()

    def get_time(self):
        self.current_format = TimeFormat(self.selected_format.get())
        self.current_color = TimeColor[self.selected_color.get()]

        if (
            self.current_format == TimeFormat.Military_Time
            or self.current_format == TimeFormat.Standard_Time
        ):
            self.time_canvas.place_forget()
            self.time_label.place(relx=0.5, rely=0.5, anchor=CENTER)
            if self.current_format == TimeFormat.Military_Time:
                string = strftime("%H:%M:%S")
            else:
                string = strftime("%I:%M:%S %p")
            self.time_label.config(
                text=string, foreground=self.current_color.value
            )
        else:
            self.time_label.place_forget()
            self.time_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.update_analog_clock()

        self.time_label.after(1, self.get_time)

    def update_analog_clock(self):
        self.time_canvas.delete("all")
        now = time.localtime()
        hour = now.tm_hour % 12
        minute = now.tm_min
        second = now.tm_sec

        # Draw clock face
        self.time_canvas.create_oval(
            2, 2, ANALOG_WIDTH, ANALOG_HEIGHT, outline="black", width=2
        )

        # Draw hour numbers
        for i in range(12):
            angle = i * math.pi / 6 - math.pi / 2
            x = ANALOG_WIDTH / 2 + 0.7 * ANALOG_WIDTH / 2 * math.cos(angle)
            y = ANALOG_HEIGHT / 2 + 0.7 * ANALOG_WIDTH / 2 * math.sin(angle)
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
            x1 = ANALOG_WIDTH / 2 + 0.8 * ANALOG_WIDTH / 2 * math.cos(angle)
            y1 = ANALOG_HEIGHT / 2 + 0.8 * ANALOG_HEIGHT / 2 * math.sin(angle)
            x2 = ANALOG_WIDTH / 2 + 0.9 * ANALOG_WIDTH / 2 * math.cos(angle)
            y2 = ANALOG_HEIGHT / 2 + 0.9 * ANALOG_HEIGHT / 2 * math.sin(angle)
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
        hour_x = ANALOG_WIDTH / 2 + 0.5 * ANALOG_WIDTH / 2 * math.cos(
            hour_angle
        )
        hour_y = ANALOG_HEIGHT / 2 + 0.5 * ANALOG_HEIGHT / 2 * math.sin(
            hour_angle
        )
        self.time_canvas.create_line(
            ANALOG_WIDTH / 2,
            ANALOG_HEIGHT / 2,
            hour_x,
            hour_y,
            fill="black",
            width=6,
        )

        # Draw minute hand
        minute_angle = (minute + second / 60) * math.pi / 30 - math.pi / 2
        minute_x = ANALOG_WIDTH / 2 + 0.7 * ANALOG_WIDTH / 2 * math.cos(
            minute_angle
        )
        minute_y = ANALOG_HEIGHT / 2 + 0.7 * ANALOG_HEIGHT / 2 * math.sin(
            minute_angle
        )
        self.time_canvas.create_line(
            ANALOG_WIDTH / 2,
            ANALOG_HEIGHT / 2,
            minute_x,
            minute_y,
            fill="black",
            width=4,
        )

        # Draw second hand
        second_angle = second * math.pi / 30 - math.pi / 2
        second_x = ANALOG_WIDTH / 2 + 0.6 * ANALOG_WIDTH / 2 * math.cos(
            second_angle
        )
        second_y = ANALOG_HEIGHT / 2 + 0.6 * ANALOG_WIDTH / 2 * math.sin(
            second_angle
        )
        self.time_canvas.create_line(
            ANALOG_WIDTH / 2,
            ANALOG_HEIGHT / 2,
            second_x,
            second_y,
            fill="red",
            width=2,
        )
