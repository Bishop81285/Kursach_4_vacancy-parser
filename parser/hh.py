import requests

from parser.base import Parser
from settings import API_URL_HH
from utils.exchange_rates_api import get_currency_rate
from vacancy import Vacancy


class HhParser(Parser):

    def __init__(self, query: str):
        """
        Конструктор класса HhParser.
        :param query: поисковый запрос
        """
        super().__init__(url=API_URL_HH, headers={"User-Agent": "HH-User-Agent"},
                         params={"text": query})

    def get_data(self) -> dict:
        """
        Метод для получения данных с API HH в виде словаря.
        :return: данные с API в виде словаря
        """
        response = requests.get(self.url, headers=self.headers, params=self.params)
        data = response.json()

        return data

    def parse_data(self) -> list:
        """
        Метод для создания списка объектов класса Vacancy из данных с API HH.
        Здесь мы унифицируем данные и валидируем их.
        :return: список объектов класса Vacancy
        """
        data = self.get_data()
        vacancies = []
        rates = {'USD': get_currency_rate('USD'), 'EUR': get_currency_rate('EUR')}

        for item in data["items"]:
            data_reduced = {}

            data_reduced['title'] = item.get('name', '...')
            data_reduced['location'] = item['area'].get('name', '...')
            data_reduced['link'] = item.get('alternate_url', '...')

            if not item['salary'] is None:
                data_reduced['salary'] = {'from': item['salary'].get('from', 0), 'to': item['salary'].get('to', 0),
                                          'currency': item['salary'].get('currency', 'RUB').upper()}
            else:
                data_reduced['salary'] = item['salary']

            data_reduced['employer'] = item['employer'].get('name', '...')
            data_reduced['description'] = item["snippet"].get('responsibility', '...')
            data_reduced['requirement'] = item['snippet'].get('requirement', '...')
            data_reduced['experience'] = item['experience'].get('name', '...')
            data_reduced['source'] = "hh.ru"

            vacancy = Vacancy(**data_reduced)
            vacancy.validate(rates)
            vacancies.append(vacancy)

        return vacancies


hh = HhParser('Python')
print(hh.get_data())
print(hh.parse_data()[0])
