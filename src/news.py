import gtts
from playsound import playsound
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen


class News:
    def __init__(self):
        self.news_url = "https://news.google.com/news/rss"
        self.Client = urlopen(self.news_url)
        self.xml_page = self.Client.read()
        self.Client.close()

        self.soup_page = soup(self.xml_page,"xml")
        self.news_list = self.soup_page.findAll("item")

    def ReadNews(self):
        news_to_read = ""
        for news in self.news_list:
            news_to_read += news.title.text

        tts = gtts.gTTS(news_to_read)
        tts.save("hello.mp3")
        playsound("hello.mp3")

news = News()
news.ReadNews()