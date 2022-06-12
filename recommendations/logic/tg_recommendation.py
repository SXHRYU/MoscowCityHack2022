import csv
from person_info import *
from dataclasses import dataclass


@dataclass
class Channel:
    name: str
    readers_count: int
    weekly_growth: int
    telemetr_url: str
    url: str

# class TopChannel(BaseChannel):
#     def __init__(self):
#         self.name = self._name
#         # self.readers_count = self._readers_count
#         # self.weekly_growth = self._weekly_growth
#         # self.telemetr_url = self._telemetr_url
#         # self.url = self._url

#     @property
#     def _name(self):
#         ...


def get_top_channels(path_to_csv):
    top_channels = []
    with open(path_to_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            top_channels.append(*row)
    return top_channels[1:]


def get_channel_recommendation(*args, **kwargs) -> Channel:
    if Person in args: ...
