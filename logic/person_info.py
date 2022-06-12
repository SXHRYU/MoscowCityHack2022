from dataclasses import dataclass


@dataclass
class AgeGroup:
    name: str
    age_range: tuple[int, int]

Children = AgeGroup('Children', (1, 18))
Young = AgeGroup('Young', (18, 35))
Adult = AgeGroup('Adult', (35, 54))
Retired = AgeGroup('Retired', (55, 150))
age_groups = [Children, Young, Adult, Retired]

class Person:
    def __init__(self,
                 client_id: str,
                 gender: str,
                 birth_date: str,
                 create_date: str,
                 name: str,
                 age: int,
                 nonresident_flag: str,
                 businessman_flag: int,
                 city: str,
                 term: str,
                 contract_sum: int,
                 product_category_name: str,
                 card_id: str,
                 card_type_name: str,
                 start_date,
                 fact_close_date,
                 purchase_sum,
                 purchase_count,
                 current_balance_avg_sum,
                 current_balance_sum,
                 current_debit_turn_sum,
                 current_credit_turn_sum,
                 card_type
                 ):
        self.client_id = client_id
        self.gender = gender
        self.birth_date = birth_date
        self.name = name
        self.age = age
        
        # возможно добавлять
        ...

    @property
    def age_group(self) -> AgeGroup:
        for age_group in age_groups:
            if self.age in range(age_group.age_range[0],
                                 age_group.age_range[1]):
                return age_group

class PersonGroup:
    def __init__(self) -> None:
        self.group_list = []
    
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
        for client in eligible_clients(gender, age, city, product_category_name, age_group):
            self.group_list.append(client)
        return self

def eligible_clients(gender, age, city, product_category_name, age_group=None):
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
