'''Поиск топ 30 быстрорастущих каналов телеграмма
по полу и по возрастным группам.

Рекомендации по таргетированию для бизнеса вынесены
в  отдельную категорию business.

Характеристические группы рекомендаций:
1) Для  мужчин. Категории каналов: авто, мото, спорт, рыбалка,
строительство и ремонт, игры,  политика, военное.
2) Для женщин.  Категории каналов: дизайн, красота  и мода,
фото, гороскоп, кулинария, рукоделие.
3) Бизнес. Категории каналов: бизнес и финансы,
недвижимость, юриспруденция.
4) Для детей. Категории каналов: игры, животные, юмор.
5) Для  молодежи. Категории каналов: блоггеры, юмор, путешествия,
музыка, фильмы, сериалы.
6) Для взрослых.  Категории каналов: здоровье, строительство и ремонт,
юмор, фильмы и сериалы.
'''


import requests
from bs4 import BeautifulSoup
from .parser_urls import (
    url_men,
    url_women,
    url_business,
    url_children,
    url_young,
    url_adult
    )


# Создаем массив url и названий конечного файла для каждой категории
url_ar = [
    url_men,
    url_women,
    url_business,
    url_children,
    url_young,
    url_adult
    ]

# Определяем параметры для доступа к сайту
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36', 'accept' : '*/*'}
    
# Составляем URL запрос
def get_html(url, params = None):
    """Возвращает ответ с сайта, с которого производится парсинг."""
    r = requests.get(url, headers = HEADERS, params = params)
    return r

# Получаем необходимые данные
def get_content(html):
    """Возвращает контент с сайта, с которого производится парсинг."""
    soup = BeautifulSoup(html, 'html.parser')

    channels1 = soup.find_all('tr', class_ = "tr_even")
    channels2 = soup.find_all('tr', class_ = 'tr_odd')
    channels = channels1 + channels2

    # Получаем в виде словаря данные о каналах
    channels_ar = []   
    count = 0
    for channel in channels:
    # Чтобы пропустить  лишние тэги сайта вводится count.
    # Лишние тэги чередуются с нужными через 1,
    # поэтому условие пропускает четные тэги.
        count+=1
        if count % 2 == 1:
        # Элемент  цена есть не для каждого канала,
        # поэтому необходимо проверять ее наличие перед использованием тэга.
            if len(channel.find_all('span', class_="kt-number kt-font-brand")) == 4:
                price =  channel.find_all('span', class_="kt-number kt-font-brand")[1].get_text()
            else:
                price = 'Не  указано'
            channels_ar.append({
                'title': channel.find('a', class_="kt-ch-title").get_text(),
                'subscribers': channel.find('span', class_="kt-number kt-font-brand text-cursor").get_text(strip = True),
                'growth': channel.find_all('span', class_="kt-number kt-number-small kt-font-success")[-1].get_text(strip = True),
                'price': price,
                'link': channel.find('a', class_="kt-ch-title").get('href')
            })     
    return channels_ar 
    
# Основная функция 
def parse(num):
    """Возвращает список ТГ-каналов для характеристических групп."""
    URL = url_ar[num-1]
    html = get_html(URL)
    channels_ar = []
    # Выполняем проверку подключения к сайту,
    # в случае неполадок сети или любых других проблем выводим Error.
    if html.status_code == 200:
        channels_ar.extend(get_content(html.text))
        return channels_ar
    else:
        print('Error')
