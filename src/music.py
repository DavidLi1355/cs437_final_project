from tkinter import CENTER, Tk, Button
import random
from playsound import playsound
import multiprocessing


class Music:
    def __init__(self, root: Tk):
        self.play_button = Button(
            root, text="Play Music", command=self.play_music_callback
        )
        self.play_button.place(relx=0.3, rely=0.1, anchor=CENTER)
        self.stop_button = Button(
            root, text="Stop Music", command=self.stop_music_callback
        )
        self.stop_button.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.music_process = None

    def play_music_callback(self):
        music_list = ["resources/crab_rave.mp3", "resources/rick_roll.mp3"]
        music_to_play = random.choice(music_list)
        self.music_process = multiprocessing.Process(
            target=playsound, args=(music_to_play,)
        )
        self.music_process.start()

    def stop_music_callback(self):
        if self.music_process is None:
            return

        self.music_process.terminate()
