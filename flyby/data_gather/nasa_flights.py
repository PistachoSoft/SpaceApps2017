# pylint:disable=missing-docstring, too-few-public-methods
import csv
import io
import warnings
from collections import namedtuple
from requests import Session
from robobrowser import RoboBrowser
from flyby import LOG

warnings.simplefilter('ignore')

KEYS = ['Mark', 'System_Timestamp', 'Latitude', 'Longitude',
        'GPS_Altitude-MSL', 'GPS_Altitude', 'Pressure_Altitude',
        'RADAR_Altitude', 'Ground_Speed', 'True_Air_Speed',
        'Indicated_Air_Speed', 'Mach_Number', 'Vertical_Speed', 'True_Heading',
        'Track_Angle', 'Drift_Angle', 'Pitch_Angle', 'Roll_Angle',
        'Slip_Angle', 'Attack_Angle', 'Static_Air_Temp', 'Dew_Point',
        'Total_Air_Temp', 'Static_Pressure', 'Dynamic_Pressure',
        'Cabin_Pressure', 'Wind_Speed', 'Wind_Direction', 'Vert_Wind_Speed',
        'Solar_Zenith_Angle', 'Aircraft_Sun_Elevation', 'Sun_Azimuth',
        'Aircraft_Sun_Azimuth']


class IWGFile(namedtuple("IWGFile", "fileo, name")):
    def __iter__(self):
        return csv.DictReader(self.fileo, fieldnames=KEYS)


class IWG:
    def __init__(self):
        session = Session()
        session.verify = False
        self.browser = RoboBrowser(session=session)
        self.link = "https://asp-archive.arc.nasa.gov/"

    def recurse_directory(self, directory, stopword):
        LOG.debug("Opening %s", directory)

        def normalize_local(directory, link):
            if self.link in link:
                return link
            else:
                return "{}{}".format(directory, link)

        self.browser.open(directory)
        for link in self.browser.find_all('a')[5:]:
            link = link.attrs['href']
            if stopword in link:
                yield directory, link
            elif link[-1] == "/":
                yield from self.recurse_directory(
                    normalize_local(directory, link), stopword)

    @property
    def iwgs(self):
        """ IWGS """
        for dirname, link in self.recurse_directory(self.link, "IWG"):
            LOG.debug("Opening {}{}".format(dirname, link))
            self.browser.open("{}{}".format(dirname, link))
            sio = io.StringIO()
            sio.write(self.browser.parsed.text)
            sio.seek(0)
            try:
                yield IWGFile(sio, dirname.replace(self.link, '').replace(
                    '/', '_'))
            except csv.Error:
                LOG.exception("Error reading csv for %s", self)

    def __iter__(self):
        yield from self.iwgs
