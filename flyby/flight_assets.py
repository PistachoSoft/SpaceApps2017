# pylint:disable=missing-docstring, too-few-public-methods
import csv
import io
import warnings
from functools import lru_cache
from requests import Session
from robobrowser import RoboBrowser

warnings.simplefilter('ignore')


class Expedition:
    def __init__(self, link):
        self.link = link
        session = Session()
        session.verify = False
        self.browser = RoboBrowser(session=session)

    def __repr__(self):
        return "Expedition {}".format(self.link)

    def recurse_directory(self, directory, stopword):
        self.browser.open(directory)
        for link in self.browser.find_all('a')[5:]:
            link = link.attrs['href']
            if stopword in link:
                yield "{}{}".format(directory, link)
            elif link[-1] == "/":
                yield from self.recurse_directory(
                    "{}{}".format(directory, link), stopword)

    @property
    def iwgs(self):
        for iwg in self.recurse_directory(self.link, "IWG"):
            self.browser.open(iwg)
            sio = io.StringIO()
            sio.write(self.browser.parsed.text)
            sio.seek(0)
            try:
                yield list(csv.reader(sio))
            except Exception as err:
                print("Error: " + err)

    @property
    def kmls(self):
        pass


class Campaign:
    def __init__(self, link):
        session = Session()
        session.verify = False
        self.browser = RoboBrowser(session=session)
        self.link = link

    @property
    @lru_cache()
    def subcampaigns(self):
        self.browser.open(self.link)
        return [a.attrs['href'] for a in self.browser.find_all('a')][5:]

    def __repr__(self):
        return "Campaign {}".format(self.link)

    def __iter__(self):
        for campaign in self.subcampaigns:
            self.browser.open("{}/{}".format(self.link, campaign))
            dates = self.browser.find_all('a')[5:]
            for date in dates:
                yield date.text, Expedition(
                    "{}/{}/{}".format(
                        self.link, campaign, date.attrs['href']))


class ASPResources:
    def __init__(self):
        self.browser = RoboBrowser()
        session = Session()
        session.verify = False
        self.browser = RoboBrowser(session=session)
        self.base_link = "https://asp-archive.arc.nasa.gov/"

    @property
    @lru_cache()
    def campaigns(self):
        self.browser.open(self.base_link)
        return set([Campaign(a.attrs["href"])
                    for a in self.browser.find_all('a')
                    if self.base_link in a.attrs["href"]])
