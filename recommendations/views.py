from django.http import HttpRequest
from django.shortcuts import render
from .logic.person_info import (
    AgeGroup,
    PersonGroup,
    Children,
    Young,
    Adult,
    Retired,
    age_groups,
)
from .logic.TG_Parser import parse
from .logic.tg_recommendation import Channel, Recommendation


# Create your views here.
def index_view(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        rec = Recommendation(
            get_product_name(request.POST),
            get_city_name(request.POST),
            get_age_range(request.POST),
            get_gender(request.POST),
            get_leads_number(request.POST)
        )
        rec.age_categories = get_age_categories(rec.age_range)
        rec.category_percents = get_category_percents(rec.age_range)
        rec.top_channels = get_top_channels(rec)
        rec.final_channels = cutoff_top_channels(rec.category_percents, rec.top_channels)
        context = {
            "recommendation": rec
        }
    return render(request, 'index.html', context)

def get_product_name(data: HttpRequest) -> str:
    for key in data.keys():
        if key.startswith('card-'):
            return key

def get_city_name(data: HttpRequest) -> str:
    return data.get('city')

def get_age_range(data: HttpRequest) -> int:
    return data.get('age-range')

def get_gender(data: HttpRequest) -> str:
    for key in data.keys():
        if key.startswith('gender-'):
            return key

def get_leads_number(data: HttpRequest) -> int:
    return data.get('number-leads')

def get_recommended_channels(group: PersonGroup, context: dict):
    group.age_range = context['age_range']
    group.city = context['city']
    group.gender = context['gender']

def get_age_categories(age_range: tuple[int, int]) -> list:
    touched_categories = []
    ages_in_age_range = get_ages_in_age_range(age_range)
    for group in age_groups:
        for age in ages_in_age_range:
            if age in range(group.age_range[0], group.age_range[1]):
                touched_categories.append(group)
                break
    return touched_categories

def get_ages_in_age_range(age_range: tuple[int, int]) -> list:
    return [i for i in range(age_range[0], age_range[1])]

def get_category_percents(age_range: dict[AgeGroup, int]) -> dict:
    ages_in_age_range = get_ages_in_age_range(age_range)
    touched_categories = get_age_categories(age_range)
    total_ages = len(ages_in_age_range)

    category_percents = dict()
    age = ages_in_age_range[0]
    category_index = 0
    
    for group in touched_categories:
        age_count = 0
        while age < ages_in_age_range[-1]:
            if age <= group.age_range[1]:
                age_count = group.age_range[1] - age + 1
                category_index += 1
                age = touched_categories[category_index].age_range[0]
                break
        category_percents[group] = age_count / total_ages
    return category_percents

def get_top_channels(recommendation: Recommendation) -> dict[str, list]:
    touched_categories = get_age_categories(recommendation.age_range)

    channels_1 = []
    channels_2 = []
    channels_3 = []
    channels_4 = []
    channels_5 = []
    channels_6 = []

    top_channels = dict()
    if recommendation.gender == 'gender-male' and Adult in touched_categories:
        channels_1.append(parse(1))
        top_channels['men'] = channels_1
    if recommendation.gender == 'gender-female' and Adult in touched_categories:
        channels_2.append(parse(2))
        top_channels['women'] = channels_2
    if recommendation.product_name == 'card-business':
        channels_3.append(parse(3))
        top_channels['business'] = channels_3
    if Children in touched_categories:
        channels_4.append(parse(4))
        top_channels['children'] = channels_4
    if Young in touched_categories:
        channels_5.append(parse(5))
        top_channels['young'] = channels_5
    if recommendation.gender == 'gender-any' and (Adult in touched_categories
                                            or Retired in touched_categories):
        channels_6.append(parse(6))
        top_channels['adult'] = channels_6
    return top_channels

def cutoff_top_channels(category_percents: dict, top_channels: dict) -> list[Channel]:

    channels_1 = []
    channels_2 = []
    channels_3 = []
    channels_4 = []
    channels_5 = []
    channels_6 = []
    displayed_channels = []

    if top_channels['men'] is not None:
        channels_1 = channels_1[0: len(top_channels['men'])*category_percents[Adult]]
    if top_channels['women'] is not None:
        channels_2 = channels_2[0: len(top_channels['women'])*category_percents[Adult]]
    if top_channels['business'] is not None:
        channels_3 = channels_3[0: len(top_channels['business'])*category_percents[Adult]]
    if top_channels['children'] is not None:
        channels_4 = channels_4[0: len(top_channels['children'])*category_percents[Children]]
    if top_channels['young'] is not None:
        channels_5 = channels_5[0: len(top_channels['young'])*category_percents[Young]]
    if top_channels['adult'] is not None:
        channels_6 = channels_6[0: len(top_channels['adult'])*(category_percents[Adult]+category_percents[Retired])]
    
    displayed_channels.append(channels_1, channels_2, channels_3, channels_4, channels_5, channels_6)
    return displayed_channels