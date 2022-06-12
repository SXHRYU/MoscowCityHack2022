#=============================================================================================
#Поиск топ 30 быстрорастущих каналов телеграмма по полу и по возрастным группам. 
#Рекомендации по таргетированию для бизнеса вынесены в  отдельную категорию buisness.
#1) Для  мужчин. Категории каналов: авто, мото, спорт, рыбалка, строительство и ремонт, игры,  политика, военное
#2) Для женщин.  Категории каналов: дизайн, красота  и мода, фото, гороскоп, кулинария, рукоделие
#3) Бизнес. Категории каналов: бизнес  и  финансы, недвижимость, юриспруденция
#4) Для детей. Категории каналов:  игры, животные, юмор
#5) Для  молодежи. Категории каналов: блоггеры, юмор, путешествия, музыка, филььмы, сериалы
#6) Для взрослых.  Категории каналов: здоровье, строительство и ремонт, юмор, фильмы и сериалы
#=============================================================================================
import requests
from bs4 import BeautifulSoup
import csv

#Создаем массив url и названий конечного файла для каждой категории
url_ar = [
    'https://telemetr.me/channels/cat/%D0%90%D0%B2%D1%82%D0%BE%20%D0%B8%20%D0%BC%D0%BE%D1%82%D0%BE,%D0%9F%D0%BE%D0%B4%D1%81%D0%BB%D1%83%D1%88%D0%B0%D0%BD%D0%BE,%D0%98%D0%B3%D1%80%D1%8B,%D0%A1%D0%BF%D0%BE%D1%80%D1%82,%D0%92%D0%BE%D0%B5%D0%BD%D0%BD%D0%BE%D0%B5,%D0%94%D0%BB%D1%8F%20%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD,%D0%9D%D0%B0%D1%83%D0%BA%D0%B0%20%D0%B8%20%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8/?order_column=participants_month&page=1',
    'https://telemetr.me/channels/cat/%D0%94%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD,%D0%9A%D1%80%D0%B0%D1%81%D0%BE%D1%82%D0%B0%20%D0%B8%20%D0%BC%D0%BE%D0%B4%D0%B0,%D0%9A%D1%83%D0%BB%D0%B8%D0%BD%D0%B0%D1%80%D0%B8%D1%8F,%D0%A0%D1%83%D0%BA%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%D0%B5,%D0%93%D0%BE%D1%80%D0%BE%D1%81%D0%BA%D0%BE%D0%BF,%D0%A4%D0%BE%D1%82%D0%BE/?order_column=participants_month&page=1&order_column=participants_month&order_direction=DESC',
    'https://telemetr.me/channels/cat/%D0%9D%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C,%D0%91%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%20%D0%B8%20%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D1%8B,%D0%AE%D1%80%D0%B8%D1%81%D0%BF%D1%80%D1%83%D0%B4%D0%B5%D0%BD%D1%86%D0%B8%D1%8F/?order_column=participants_month&page=1',
    'https://telemetr.me/channels/cat/%D0%98%D0%B3%D1%80%D1%8B,%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5/?order_column=participants_month&page=1',
    'https://telemetr.me/channels/cat/%D0%91%D0%BB%D0%BE%D0%B3%D0%B3%D0%B5%D1%80%D1%8B,%D0%9F%D1%83%D1%82%D0%B5%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%8F,%D0%9C%D1%83%D0%B7%D1%8B%D0%BA%D0%B0,%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5,%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B/?order_column=participants_month&page=1#',
    'https://telemetr.me/channels/cat/%D0%97%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D1%8C%D0%B5,%D0%A1%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE%20%D0%B8%20%D1%80%D0%B5%D0%BC%D0%BE%D0%BD%D1%82,%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5,%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B/?order_column=participants_month&page=1'
    ]
filename_ar = [
    'tg_men.csv', 
    'tg_women.csv',
    'tg_buisness.csv', 
    'tg_kids.csv', 
    'tg_youth.csv', 
    'tg_adult.csv'
    ]

#Определяем параметры для доступа к сайту
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36', 'accept' : '*/*'}

#Функция для выбора категории
def category_num():
    num = int(input('Input number to choose category: 1 - men, 2 - women, 3 - buisness, 4 - kids, 5 - youth, 6 - adult: '))
    if num < 1 or num > 6:
        print('Error.  Number must be in range from 1 to 6')
        return category_num()
    else:
        return num
    
#Составляем URL запрос
def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

#Получаем необходимые данные
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    channels1 = soup.find_all('tr', class_ = "tr_even")
    channels2 = soup.find_all('tr', class_ = 'tr_odd')
    channels = channels1+channels2
#Получаем в виде словаря данные о каналах
    channels_ar = []   
    count = 0
    for channel in channels:
#Чтобы пропустить  лишние тэги сайта вводится count. Лишние тэги чередуются с нужными через 1, поэтому условие пропускает четные тэги.
        count+=1
        if count % 2 == 1:
#Элемент  цена есть  не  для каждого канала,  поэтому необходимо  проверять ее наличие перед  использованием тэга
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

#Функция для сохранения данных в csv таблицу
def save_file(items, path):
    with open(path, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название канала','Число подписчиков','Прирост подписчиков за месяц','Стоимость  одного поста','Ссылка на канал'])
        for item in items:
            writer.writerow([item['title'], item['subscribers'], item['growth'], item['price'], item['link']])
    
#Основная функция 
def parse():
    num = category_num()
    URL = url_ar[num-1]
    FILE = filename_ar[num-1]
    html = get_html(URL)
    channels_ar = []
#Выполняем проверку подключения к сайту, в случае неполадок сети или любых других проблем выводим Error
    if html.status_code == 200:
        channels_ar.extend(get_content(html.text))
        save_file(channels_ar , FILE)
        print('Done successfully!')
    else:
        print('Error')
parse()