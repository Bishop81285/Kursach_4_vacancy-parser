import os

import requests

from parser.base import Parser
from settings import API_URL_SJ
from utils.exchange_rates_api import get_currency_rate
from vacancy import Vacancy


class SjParser(Parser):

    __SJ_API_TOKEN: str = os.getenv('SJ_API_TOKEN')

    def __init__(self, query: str, page: int):
        """
        Конструктор класса SjParser.
        :param query: поисковый запрос
        :param page: кол-во страниц для обработки
        """
        super().__init__(url=API_URL_SJ, headers={"X-Api-App-Id": self.__SJ_API_TOKEN},
                         params={"keyword": query, "count": 50, 'page': page})

    def get_data(self) -> dict:
        """
        Метод для получения данных с API SJ в виде словаря.
        :return: данные с API в виде словаря
        """
        response = requests.get(self.url, headers=self.headers, params=self.params)

        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 400:
            raise ValueError("Неверные параметры запроса")
        elif response.status_code == 404:
            raise ValueError("Нет данных по указанному запросу")
        else:
            raise ValueError(f"Произошла ошибка при обращении к API HH: {response.status_code}")

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

