import os

import requests

from parser.base import Parser
from settings import API_URL_SJ
from utils.exchange_rates_api import get_currency_rate
from vacancy import Vacancy


class SjParser(Parser):

    __SJ_API_TOKEN: str = os.getenv('SJ_API_TOKEN')

    def __init__(self, query: str):
        """
        Конструктор класса SjParser.
        :param query: поисковый запрос
        """
        super().__init__(url=API_URL_SJ, headers={"X-Api-App-Id": self.__SJ_API_TOKEN},
                         params={"keyword": query, "count": 50})

    def get_data(self) -> dict:
        """
        Метод для получения данных с API SJ в виде словаря.
        :return: данные с API в виде словаря
        """
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data = response.json()

        return data

    def parse_data(self) -> list:
        """
        Метод для создания списка объектов класса Vacancy из данных с API SJ.
        Здесь мы унифицируем данные и валидируем их.
        :return: список объектов класса Vacancy
        """
        data = self.get_data()
        vacancies = []
        rates = {'USD': get_currency_rate('USD'), 'EUR': get_currency_rate('EUR')}

        for item in data["objects"]:
            data_reduced = {}

            data_reduced['title'] = item.get('profession', '...')
            data_reduced['location'] = item['town'].get('title', '...')
            data_reduced['link'] = item.get('link', '...')
            data_reduced['employer'] = item.get('firm_name', '...')
            data_reduced['salary'] = {'from': item.get('payment_from', 0), 'to': item.get('payment_to', 0),
                                      'currency': item.get('currency', 'RUB').upper()}
            data_reduced['description'] = item.get('candidat', '...')
            data_reduced['requirement'] = '...'
            data_reduced['experience'] = item['experience'].get('title', '...')
            data_reduced['source'] = "superjob.ru"

            vacancy = Vacancy(**data_reduced)
            vacancy.validate(rates)
            vacancies.append(vacancy)

        return vacancies


sj = SjParser('Python')
# print(sj.get_data())
print(len(sj.parse_data()))
print(sj.parse_data()[0])
