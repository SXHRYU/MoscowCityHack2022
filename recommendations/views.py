from django.http import HttpRequest
from django.shortcuts import render
from .cities import cities
from .logic.person_info import (
    AgeGroup,
    Children,
    Young,
    Adult,
    Retired,
    age_groups,
)
from .logic.tg_parser import parse
from .logic.tg_recommendation import Channel, Recommendation


# Основной алгоритм обработки формы:
# 1)на вход получаем словарь request.POST с данными из формы;
# 2)достаём из словаря значения:
#       продукта, города, возрастов, пола и кол-ва лидов;
# 3)рассчитываем возрастные категории,
#       в которые попадает диапазон возрастов;
# 4)рассчитываем процентное соотношение
#       включённых возрастов в каждой возрастной группе
#       к общему кол-ву запрошенных возрастов;
# 5)получаем самые популярные тг-каналы
#       для характеристических (не возрастных) групп;
# 6)отсекаем кол-во популярных каналов
#       в соответствии с процентными соотношениями из пункта 4;
# 7)выводим оставшиеся каналы пользователю;
# 8)считаем и выводим бюджет согласно принятой модели.
def index_view(request: HttpRequest):
    """Функция-контроллёр, отправляющая пользователю HTML-страницу.
    
    Форма обрабатывается в условии `if request.method == 'POST'`.
    """
    # Возвращает список городов для выбора города в форме.
    cities_list = cities.split(' ')
    context = {'cities_list': cities_list}
    # Обрабатываем форму в POST-запросе.
    if request.method == 'POST':
        # Расчёт необходимых данных рекомендации.
        # Было решено хранить все значения в объекте рекомендации,
        # а не отдельными переменами, для возможного расширения и/или
        # модификаций самого объекта.
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
        rec.budget = count_budget(rec)
        # Возвращает конечный список каналов для рекламы.
        list_of_recommended_channels = [j for i in range(len(rec.final_channels)) for j in rec.final_channels[i]]
        context = {
            "recommendation": rec,
            "recommended_channels": list_of_recommended_channels,
            "cities_list": cities_list,
            "recommendation": rec,
        }
    # Отправляем пользователю страницу с рассчитанными значениями.
    return render(request, 'index.html', context)

def get_product_name(data: HttpRequest) -> str:
    """Возвращает название продукта из формы.
    
    Результат представлен в виде:
    'card-business' | 'card-debit' | 'card-credit'.
    """
    for key in data.keys():
        if key.startswith('card-'):
            return key

def get_city_name(data: HttpRequest) -> str:
    """Возвращает город из формы."""
    return data.get('city')

def get_age_range(data: HttpRequest) -> str:
    """Возвращает диапазон значений возраста из формы.
    
    Результат представлен в виде ('18 лет - 30 лет').
    Нормализацией и приведением к виду (18, 30) занимается
    метод 'tuplise_age_range' класса Recommendation.
    """
    return data.get('age-range')

def get_gender(data: HttpRequest) -> str:
    """Возвращает пол из формы в виде 

    Результат представлен в виде:
    'gender-any' | 'gender-male' | 'gender-female'.
    """ 
    for key in data.keys():
        if key.startswith('gender-'):
            return key

def get_leads_number(data: HttpRequest) -> int:
    """Возвращает кол-во лидов."""
    return int(data.get('number-leads'))

def get_age_categories(age_range: tuple[int, int]) -> list[AgeGroup]:
    """Возвращает возрастные категории,
    в которые входит запрошенный диапазон возрастов.

    Результат представлен в виде:
    [AgeGroup('Children', age_range=(6, 18)), ...]
    """
    touched_categories = []
    ages_in_age_range = get_ages_in_age_range(age_range)
    for group in age_groups:
        for age in ages_in_age_range:
            if age in range(group.age_range[0], group.age_range[1]):
                touched_categories.append(group)
                break
    return touched_categories

def get_ages_in_age_range(age_range: tuple[int, int]) -> list:
    """Возвращает все возрасты, входящие в запрошенный диапазон."""
    return [i for i in range(age_range[0], age_range[1])]

def get_category_percents(age_range: tuple[int, int]) -> dict[AgeGroup, int]:
    """Возвращает процентное соотношение запрошенных возрастов,
    входящих в разные группы.

    То есть для диапазона (25, 45) результат будет 
    {
        AgeGroup('Young', (18, 35)): 0.5,
        AgeGroup('Adult', (35, 45)): 0.5,
    }
    потому что диапазон (25, 45) на 50% входит в диапазон Young
    и на 50% в диапазон Adult
    """
    ages_in_age_range = get_ages_in_age_range(age_range)
    touched_categories = get_age_categories(age_range)
    total_ages = len(ages_in_age_range)

    category_percents = dict()

    for group in touched_categories:
        age_count = 0
        ages_set = set(ages_in_age_range)
        age_group_set = set(range(group.age_range[0], group.age_range[1]))
        age_count += len(ages_set.intersection(age_group_set))
        category_percents[group] = age_count / total_ages
        
    return category_percents

def get_top_channels(recommendation: Recommendation) -> dict[str, Channel]:
    """Возвращает самые популярные каналы по характеристическим группам
    (не возрастным).

    Характеристические группы описаны в файле TG_parser.py.
    Результат представлен в виде: 
    [
        {'men': [[{Channel_1}, {Channel_2}, ...]]},
        {'women': [[{Channel_1}, {Channel_2}, ...]]},
        ...
    ]
    """
    touched_categories = get_age_categories(recommendation.age_range)

    channels_1 = []
    channels_2 = []
    channels_3 = []
    channels_4 = []
    channels_5 = []
    channels_6 = []

    top_channels = dict()
    print('\nParsing telegram channels...')
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
    print('\nDone parsing...')
    return top_channels

def cutoff_top_channels(category_percents: dict, top_channels: dict) -> list[Channel]:
    """Возвращает кол-во каналов, пропорциональное кол-ву людей в
    соответствующих характеристических группах.
    
    Результат представлен в виде [{Channel_1}, {Channel_2}, ...]
    """
    channels_1 = []
    channels_2 = []
    channels_3 = []
    channels_4 = []
    channels_5 = []
    channels_6 = []
    displayed_channels = []
    # Использование характеристических групп - это временное решение.
    # Из-за нехватки времени на обучение модели было решено разделить
    # людей на группы по интересам.
    if top_channels.get('men') is not None:
        channels_1 = top_channels['men'][0][0: round(len(top_channels['men'][0])*category_percents[Adult])]
        displayed_channels.append(channels_1)
    if top_channels.get('women') is not None:
        channels_2 = top_channels['women'][0][0: round(len(top_channels['women'][0])*category_percents[Adult])]
        displayed_channels.append(channels_2)
    if top_channels.get('business') is not None:
        channels_3 = top_channels['business'][0][0: round(len(top_channels['business'][0])*category_percents[Adult])]
        displayed_channels.append(channels_3)
    if top_channels.get('children') is not None and top_channels.get('business') is None:
        channels_4 = top_channels['children'][0][0: round(len(top_channels['children'][0])*category_percents[Children])]
        displayed_channels.append(channels_4)
    if top_channels.get('young') is not None and top_channels.get('business') is None:
        channels_5 = top_channels['young'][0][0: round(len(top_channels['young'][0])*category_percents[Young])]
        displayed_channels.append(channels_5)
    if top_channels.get('adult') is not None:
        channels_6 = top_channels['adult'][0][0: round(len(top_channels['adult'][0])*(category_percents[Adult]+category_percents.get(Retired, 0)))]
        displayed_channels.append(channels_6)

    return displayed_channels

def count_budget(recommendation: Recommendation) -> int:
    """Возвращает значение максимального бюджета,
    который возможно выделить на рекламную кампанию.
    """
    category_percents = recommendation.category_percents
    leads = recommendation.leads_number

    total_budget = 0
    # Использование усреднённых значений - это временное решение.
    # В конечной версии продукта модель машинного обучения
    # будет выдавать значения бюджета и дохода
    # по задаваемым параметрам напрямую.
    for key, value in category_percents.items():
        if key.name == 'Children':
            total_budget += value * Children.income / Children.average_hold
        elif key.name == 'Young':
            total_budget += value * Young.income / Young.average_hold
        elif key.name == 'Adult':
            total_budget += value * Adult.income / Adult.average_hold
        elif key.name == 'Retired':
            total_budget += value * Retired.income / Retired.average_hold
    return int(total_budget * leads)
