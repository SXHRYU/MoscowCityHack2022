import csv
from dataclasses import dataclass
from .person_info import *


@dataclass
class Channel:
    name: str
    readers_count: int
    weekly_growth: int
    telemetr_url: str
    url: str

class Recommendation:
    def __init__(self, 
                 product_name: str,
                 city: str,
                 age_range: tuple[int, int],
                 gender: str,
                 leads_number: str):
        self.product_name = product_name
        self.city = city
        self.age_range = self.tuplise_age_range(age_range)
        self.gender = gender
        self.leads_number = leads_number

    def tuplise_age_range(self, age_range):
        return tuple(map(int, [i for i in age_range.split(' ') if i.isdigit()]))


def get_top_channels(path_to_csv):
    top_channels = []
    with open(path_to_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            top_channels.append(*row)
    return top_channels[1:]


def get_channel_recommendation(*args, **kwargs) -> Channel:
    if Person in args: ...
