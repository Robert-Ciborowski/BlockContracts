import requests
from bs4 import BeautifulSoup


class GetWebSiteStrings:

    def __init__(self, url):
        self.link = url

    def gatherer(self, file_name):
        source_code = requests.get(self.link)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="lxml")
        print(soup)

