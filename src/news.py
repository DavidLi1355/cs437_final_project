from tkinter import Tk, Button
import gtts
from playsound import playsound
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from threading import Thread, Condition
from queue import Queue


class NewsHandler:
    @staticmethod
    def read_news_handler(work_queue: Queue):
        while True:
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
        self.play_button.pack()
        self.news_url = "https://news.google.com/news/rss"
        self.Client = urlopen(self.news_url)
        self.xml_page = self.Client.read()
        self.Client.close()

        self.soup_page = soup(self.xml_page, "xml")
        self.news_list = self.soup_page.findAll("item")

        self.work_queue = Queue()
        self.read_thread = Thread(
            target=NewsHandler.read_news_handler, args=(self.work_queue,)
        )
        self.read_thread.start()

    def read_news_callback(self):
        news_to_read = ""
        for idx, news in enumerate(self.news_list):
            if idx >= News.news_to_read:
                break
            news_to_read += news.title.text
        self.work_queue.put(news_to_read)
