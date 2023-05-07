import socket
import tkinter as tk
import queue


def run_server(time_display, alarm):

    HOST = ''  # The server's hostname or IP address
    PORT = 5000  # The port used by the server

    q = queue.Queue()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:

            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # check command in data

                    print(data.decode())
                    tasks = data.decode().split('\n')
                    for t in tasks:
                        q.put(t)

                    while not q.empty():
                        words = q.get()
                        words = words.split(' ')
                        print(words)
                        if words[0] == 'SET_ALARM':
                            alarm.hour_text.delete(0, tk.END)
                            alarm.minute_text.delete(0, tk.END)

                            alarm.hour_text.insert(0, words[1])
                            alarm.minute_text.insert(0, words[2])
                            alarm.set_alarm()
                        if words[0] == 'RESET_ALARM':
                            alarm.reset_alarm()
                        if words[0] == 'FORMAT':
                            time_display.selected_format.set(" ".join(words[1:]))
                        if words[0] == 'COLOR':
                            time_display.selected_color.set(words[1])