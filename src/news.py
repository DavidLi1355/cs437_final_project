from tkinter import CENTER, Tk, Button
import gtts
from playsound import playsound
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from threading import Thread, Event
from queue import Queue


class NewsHandler:
    @staticmethod
    def read_news_handler(work_queue: Queue, event: Event):
        while True:
            if event.isSet():
                break
            news_to_read: str = work_queue.get()
            tts = gtts.gTTS(news_to_read)
            tts.save("news.mp3")
            playsound("news.mp3")


class News:
    news_to_read = 3

    def __init__(self, root: Tk):
        self.play_button = Button(
            root, text="Play News", command=self.read_news_callback
        )
        self.play_button.place(relx=0.7, rely=0.1, anchor=CENTER)

        self.news_url = "https://news.google.com/news/rss"
        self.Client = urlopen(self.news_url)
        self.xml_page = self.Client.read()
        self.Client.close()

        self.soup_page = soup(self.xml_page, "xml")
        self.news_list = self.soup_page.findAll("item")

        self.event = Event()
        self.work_queue = Queue()
        self.read_thread = Thread(
            target=NewsHandler.read_news_handler,
            args=(
                self.work_queue,
                self.event,
            ),
        )
        self.read_thread.start()

    def __del__(self):
        self.event.set()
        self.work_queue.put("")
        self.read_thread.join()

    def read_news_callback(self):
        news_to_read = ""
        for idx, news in enumerate(self.news_list):
            if idx >= News.news_to_read:
                break
            news_to_read += str(idx + 1) + "\n" + news.title.text + "\n"
        self.work_queue.put(news_to_read)
