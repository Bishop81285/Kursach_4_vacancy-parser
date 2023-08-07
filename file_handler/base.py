from abc import ABC, abstractmethod


class FileHandler(ABC):

    def __init__(self, filename: str):
        """
        Конструктор класса FileHandler.
        :param filename: имя файла
        """
        self.__filename = filename

    @property
    def filename(self):
        return self.__filename

    @abstractmethod
    def add_vacancies(self, vacancies: list):
        """
        Метод для добавления списка вакансий в файл.
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        pass

    @abstractmethod
    def get_vacancies(self, **keywords) -> list:
        """
        Метод для возвращения списка вакансий из файла по указанным критериям.
        :param keywords: словарь с критериями для фильтрации вакансий
        :return: список объектов класса Vacancy, удовлетворяющих критериям
        """
        pass

    @abstractmethod
    def delete_vacancies(self, vacancies: list):
        """
        Метод для удаления списка вакансий из файла.
        :param vacancies: список объектов класса Vacancy
        :return:
        """
        pass
