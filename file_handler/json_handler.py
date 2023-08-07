import json

from file_handler.base import FileHandler
from settings import DATA_PATH
from vacancy import Vacancy


class JsonHandler(FileHandler):

    __file_path = str(DATA_PATH) + '/'

    def __init__(self, filename: str):
        """
        Конструктор класса JsonHandler.
        :param filename: имя файла
        """
        super().__init__(filename)

    def __len__(self) -> int:
        """
        Метод для возвращения длины списка вакансий в файле
        :return: длину списка
        """
        with open(self.__file_path + self.filename, "r", encoding="utf-8") as file:
            json_data = file.read()

        data = json.loads(json_data)

        return len(data)

    def add_vacancies(self, vacancies: list):
        """
        Метод для добавления списка вакансий в файл.
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        data = self.transform_to_json(vacancies)

        json_data = json.dumps(data, ensure_ascii=False, indent=4)

        with open(self.__file_path + self.filename, "w", encoding="utf-8") as file:
            file.write(json_data)

    def get_vacancies(self, **keywords) -> list:
        """
        Метод для возвращения списка вакансий из файла по указанным критериям.

        Если критерии не указаны, то возвращает список всех вакансий в файле
        :param keywords: словарь с критериями для фильтрации вакансий
        :return: список объектов класса Vacancy, удовлетворяющих критериям
        """
        with open(self.__file_path + self.filename, "r", encoding="utf-8") as file:
            json_data = file.read()

        data = json.loads(json_data)
        vacancies = [Vacancy(**vacancy) for vacancy in data]

        if not keywords:
            return vacancies

        filtered_vacancies = []

        for vacancy in vacancies:
            match = True

            for key, value in keywords.items():
                if key == "city":
                    if vacancy.location.lower() != value.lower():
                        match = False
                        break
                elif key == "employer":
                    if vacancy.employer.lower() != value.lower():
                        match = False
                        break
                elif key == "salary":
                    if vacancy.salary_from < value["from"] or vacancy.salary_to > value["to"]:
                        match = False
                        break
                elif key == "description":
                    if not any(word in vacancy.description.lower() for word in value):
                        match = False
                        break
                elif key == "requirements":
                    if not any(word in vacancy.requirement.lower() for word in value):
                        match = False
                        break
                elif key == "source":
                    if vacancy.source.lower() != value.lower():
                        match = False
                        break

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    @staticmethod
    def transform_to_json(vacancies: list) -> list[dict]:
        """
        Преобразование списка объектов в список словарей
        :param vacancies: список объектов класса Vacancy
        :return: список словарей с вакансиями
        """
        vacancies_dict = []

        for vacancy in vacancies:
            vacancy_dict = {
                'title': vacancy.title,
                'location': vacancy.location,
                'link': vacancy.link,
                'employer': vacancy.employer,
                'salary': vacancy.get_salary(),
                'description': vacancy.description,
                'requirement': vacancy.requirement,
                'experience': vacancy.experience,
                'source': vacancy.source
            }

            vacancies_dict.append(vacancy_dict)

        return vacancies_dict

    def delete_vacancies(self, vacancies: list):
        """
        Метод для удаления списка вакансий из файла.
        :param vacancies: список объектов класса Vacancy
        :return: None
        """
        with open(self.__file_path + self.filename, "r", encoding="utf-8") as file:
            json_data = file.read()

        data = json.loads(json_data)
        vacancies_dict = self.transform_to_json(vacancies)

        updated_data = [vacancy for vacancy in data if vacancy not in vacancies_dict]
        updated_json_data = json.dumps(updated_data, ensure_ascii=False, indent=4)

        with open(self.__file_path + self.filename, "w", encoding="utf-8") as file:
            file.write(updated_json_data)
