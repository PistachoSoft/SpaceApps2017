# pylint:disable=missing-docstring, too-few-public-methods
import csv
import io
import warnings
from functools import lru_cache
from requests import Session
from robobrowser import RoboBrowser

warnings.simplefilter('ignore')

KEYS = ['System_Timestamp',  'Latitude',  'Longitude',  'GPS_Altitude-MSL',
        'GPS_Altitude',  'Pressure_Altitude',  'RADAR_Altitude',
        'Ground_Speed',  'True_Air_Speed',  'Indicated_Air_Speed',
        'Mach_Number',  'Vertical_Speed',  'True_Heading',  'Track_Angle',
        'Drift_Angle',  'Pitch_Angle',  'Roll_Angle',  'Slip_Angle',
        'Attack_Angle',  'Static_Air_Temp',  'Dew_Point',  'Total_Air_Temp',
        'Static_Pressure',  'Dynamic_Pressure',  'Cabin_Pressure',
        'Wind_Speed',  'Wind_Direction',  'Vert_Wind_Speed',
        'Solar_Zenith_Angle',  'Aircraft_Sun_Elevation',  'Sun_Azimuth',
        'Aircraft_Sun_Azimuth']

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

    @staticmethod
    def parse_iwg(iwg):
        self.browser.open(iwg)
        sio = io.StringIO()
        sio.write(self.browser.parsed.text)
        sio.seek(0)
        try:
            yield list(csv.DictReader(sio, fieldnames=KEYS))
        except Exception as err:
            print("Error: " + err)

    @property
    def iwgs(self):
        return (parse_iwg(i) for i in self.recurse_directory(self.link, "IWG"))

    @property
    def kmls(self):
        pass

    def videos(self):
        yield from self.recurse_directory(self.link 'avi')


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
