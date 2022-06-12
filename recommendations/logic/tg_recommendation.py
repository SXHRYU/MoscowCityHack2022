from dataclasses import dataclass


@dataclass
class Channel:
    """Объект Телеграм канала.
    
    Используется в основном для type hinting.
    В функциях представлен в виде словаря:
    {'title': '...'}, {'subscribers': ...}, ...
    """
    title: str
    subscribers: int
    weekly_growth: int
    ad_price: int
    telemetr_url: str

class Recommendation:
    """Объект рекомендации.

    Используется в основном для type hinting.
    Содержит в себе все основные параметры, получаемые из POST-запроса.
    """
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

    def tuplise_age_range(self, age_range) -> tuple[int, int]:
        """Возвращает нормализованный кортеж запрошенных возрастов.
        
        На вход получает строку "('16 лет - 20 лет')", возвращает
        (16, 20).
        """
        return tuple(map(int, [i for i in age_range.split(' ') if i.isdigit()]))
