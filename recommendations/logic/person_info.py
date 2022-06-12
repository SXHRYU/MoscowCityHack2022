from dataclasses import dataclass


@dataclass
class AgeGroup:
    """Объект возрастных групп.

    Представлен в виде:
    AgeGroup(name='Children', age_range=(1, 18))
    """
    name: str
    age_range: tuple[int, int]

    # Необходимо, чтобы использовать как ключи в словаре.
    def __hash__(self) -> int:
        return hash(repr(self))

# Возрастные группы.
# Предоставляют интерфейс для изменения
# пар-ов расчёта коэффициентов и выдачи соответствующих ТГ-каналов.
Children = AgeGroup('Children', (6, 18))
Young = AgeGroup('Young', (18, 35))
Adult = AgeGroup('Adult', (35, 65))
Retired = AgeGroup('Retired', (65, 70))
age_groups = [Children, Young, Adult, Retired]

class Person:
    """Объект человека.
    
    Представлен в основном для type hinting.
    Использовался в тестовых целях.
    """
    def __init__(self,
                 client_id: str,
                 gender: str,
                 birth_date: str,
                 name: str,
                 age: int,
                 ):
        self.client_id = client_id
        self.gender = gender
        self.birth_date = birth_date
        self.name = name
        self.age = age
        # возможно добавлять новые параметры
        ...

    @property
    def age_group(self) -> AgeGroup:
        for age_group in age_groups:
            if self.age in range(age_group.age_range[0],
                                 age_group.age_range[1]):
                return age_group

class PersonGroup:
    """Объект запрошенных групп людей.

    Изначально использовался для выдачи рекомендаций, затем был изменён
    на более прямой объект Recommendation.
    Использовался в тестовых целях.
    """
    def __init__(self, age_range, city, gender) -> None:
        self.group_list = []
        self.age_range = age_range
        self.city = city
        self.gender = gender
    
    def add_person(self, person: Person) -> 'PersonGroup':
        self.group_list.append(person)
        return self
    
    def delete_person(self, person: Person) -> 'PersonGroup':
        self.group_list.remove(person)
        return self

    def generate_group_by_params(self, **kwargs) -> 'PersonGroup':
        gender = kwargs.get('gender')
        age = kwargs.get('age')
        age_group = kwargs.get('age_group')
        city = kwargs.get('city')
        product_category_name = kwargs.get('product_category_name')
        for client in eligible_clients(gender,
                                       age,
                                       city,
                                       product_category_name,
                                       age_group):
            self.group_list.append(client)
        return self

def eligible_clients(gender, age, city, product_category_name, age_group=None):
    """Возвращает клиентов, подходящих под определённые характеристики.
    """
    import csv
    if age_group is not None:
        age = None
    else:
        age_group = None
    with open('C:/Users/user/Desktop/hackathon/Условие/Данные по транзакционной активности клиентов.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if (
                row[1] == gender
                and ((2022 - int(row[2])) == age or 
                    (2022 - int(row[2])) in range(age_group.age_range[0],
                                            age_group.age_range[1]))
                and row[6] == city
                and row[9] == product_category_name
                ):
                yield row
