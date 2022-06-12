import requests
from bs4 import BeautifulSoup
import csv
#Создаем необходимые константы для запроса
URL = 'https://telemetr.me'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36', 'accept' : '*/*'}
#Будущее имя csv таблицы результатов
FILE = 'tg.csv'

#Составляем URL запрос
def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

#Получаем необходимые данные
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
#Выделяем категорию каналов с наибольшим приростом подписчиков за неделю
    week_ch = str(soup.find_all('div', id = "channels_sub_week")[0])
    soup_ch = BeautifulSoup(week_ch, 'html.parser')
    channels = soup_ch.find_all('div', class_="kt-widget4__item p-2 pl-3 pr-3")
#Получаем в виде словаря данные о канале
    channels_ar = []
    for channel in channels:
        channels_ar.append({
            'title': channel.find('a', class_="kt-widget4__title").get_text(strip = True),
            'subscribers': channel.find('span', class_="kt-font-boldest kt-font-dark").get_text(strip = True),
            'growth': channel.find('span', class_="kt-widget4__number kt-font-success").get_text(strip = True),
            'link': ( URL + str(channel.find('a', class_="kt-widget4__title").get('href')))
            })
    return channels_ar 

#Функция для сохранения данных в csv таблицу
def save_file(items, path):
    with open(path, 'w', newline = '', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название канала','Число подписчиков','Прирост подписчиков за неделю','Ссылка на анализ канала'])
        for item in items:
            writer.writerow([item['title'], item['subscribers'], item['growth'], item['link']])
    
#Основная функция 
def parse():
    html = get_html(URL)
    channels_ar = []
#Выполняем проверку подключения к сайту, в случае неполадок сети или любых других проблем выводим Error
    if html.status_code == 200:
        channels_ar.extend(get_content(html.text))
        save_file(channels_ar , FILE)
    else:
        print('Error')
parse()