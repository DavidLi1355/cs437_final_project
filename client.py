from tkinter import Tk, mainloop
from src.time_display import TimeDisplay
from src.alarm import Alarm
import socket
from src.speech_to_text import SpeechToText

# setup root
root = Tk()
root.geometry("700x900")
root.resizable(False, False)
root.title("Clock")

# setup clock and alarm
HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000  # The port used by the server
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

time_display = TimeDisplay(root, is_client=True)
time_display.get_time()
alarm = Alarm(root, is_client=True)
time_display.set_socket(socket)
alarm.set_socket(socket)

mainloop()
