from abc import ABC, abstractmethod


class Parser(ABC):

    def __init__(self, url: str, headers: dict, params: dict):
        """
        Конструктор класса Parser.
        :param url: адрес API
        :param headers: заголовки запроса
        :param params: параметры запроса
        """
        self.__url = url
        self.__headers = headers
        self.__params = params

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    @property
    def params(self):
        return self.__params

    @abstractmethod
    def get_data(self) -> dict:
        """
        Метод для получения данных с API в виде словаря.
        :return: данные с API в виде словаря
        """
        pass

    @abstractmethod
    def parse_data(self) -> list:
        """
        Метод для создания списка объектов класса Vacancy из данных с API.
        :return: список объектов класса Vacancy
        """
        pass
