from urllib.request import urlopen

from bs4 import BeautifulSoup as bs

import textwrap

import os

import re


class Scraper:
    def __init__(self):
        self.headline_content = []
        self.pages = {
            "avaleht": "http://www.delfi.ee/",
            "sport": "http://www.delfi.ee/sport",
            "forte": "http://www.forte.delfi.ee/",
            "arileht": "http://www.arileht.delfi.ee/"
        }
        print("""             _____  ______ _      ______ _____ 
            |  __ \|  ____| |    |  ____|_   _|
            | |  | | |__  | |    | |__    | |  
            | |  | |  __| | |    |  __|   | |  
            | |__| | |____| |____| |     _| |_ 
            |_____/|______|______|_|    |_____|                                                    
            DELFI.EE terminalibrauser
        """)
        self.user_action()

    def get_window_width(self):
        return os.get_terminal_size().columns

    def user_action(self):
        while True:
            print("\n" + self.get_window_width() * "_")
            action = input("Delfi uudised: [avaleht, sport, forte, arileht]\n"
                           "Stop: [q],\n"
                           "Artikkel: [number]\n")
            if action == "q":
                break
            elif action in self.pages.keys():
                os.system("cls")
                print(action.upper() + "\n")
                print(self.get_headlines(self.pages[action]))
                continue
            try:
                os.system("cls")
                if len(self.headline_content) != 0 and 0 < int(action) < len(self.headline_content):
                    print(self.article(int(action)))
            except ValueError:
                continue

    def get_headlines(self, url):
        result = ""
        self.headline_content = []
        with urlopen(url) as page:
            html = bs(page, "html.parser")
            headlines = html.find_all("h1", {"class": "headline__title"})

            for news in headlines:
                new = [news.a.string, news.a["href"]]

                if new not in self.headline_content:
                    self.headline_content.append(new)
                    number = headlines.index(news) + 1
                    result += f"{' ' * (3-len(str(number)))}{number}. {textwrap.fill(news.a.string, width=self.get_window_width())}\n"

        return result

    def article(self, index_of_article):
        url = self.headline_content[index_of_article - 1]

        with urlopen(url[1]) as page:
            html = bs(page, "html.parser")
            lead = str(html.find_all("p", {"class": "article__chunk article__chunk--lead"})[0]).split(">")[1].strip("</p>")
            body = html.find_all("div", {"class": "article__body"})[0].find_all("p")

            final_body = ""
            for paragraph in body:
                final_body += re.sub(r"<\/?\w+>", "",
                                     textwrap.fill(str(paragraph), width=self.get_window_width()) + "\n" + "\n")

            return str(url[0]) + "\n" + "\n" + lead.strip() + "\n" + "\n" + final_body + url[1]


scraper = Scraper()
