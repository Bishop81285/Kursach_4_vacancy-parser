class Vacancy:

    __slots__ = ('__title', '__location', '__link', '__employer', '__salary',
                 '__description', '__requirement', '__experience', '__source')

    def __init__(self, **kwargs):
        """
        Конструктор класса Vacancy.
        :param kwargs: словарь с приведенными к единому формату данными по вакансии
        """
        self.__title: str = kwargs['title']
        self.__location: str = kwargs['location']
        self.__link: str = kwargs['link']
        self.__employer: str = kwargs['employer']
        self.__salary: dict = kwargs['salary']
        self.__description: str = kwargs['description']
        self.__requirement: str = kwargs['requirement']
        self.__experience: str = kwargs['experience']
        self.__source: str = kwargs['source']

    @property
    def title(self):
        return self.__title

    @property
    def location(self):
        return self.__location

    @property
    def link(self):
        return self.__link

    @property
    def employer(self):
        return self.__employer

    @property
    def salary(self):
        return self.__salary

    @property
    def description(self):
        return self.__description

    @property
    def requirement(self):
        return self.__requirement

    @property
    def experience(self):
        return self.__experience

    @property
    def source(self):
        return self.__source

    def __str__(self) -> str:
        """
        Метод для возвращения строкового представления объекта.
        :return: строковое представление объекта
        """
        return (f'Вакансия: {self.__title} | {self.__location} | {self.__link} |'
                f' {self.__employer} | {self.__salary} | {self.__description} |'
                f' {self.__requirement} | {self.__experience} | {self.__source}')

    def __repr__(self) -> str:
        """
        Метод для возвращения строкового представления объекта при отладке программы.
        :return: строковое представление объекта
        """
        return f'{self.__class__.__name__}: {self.__slots__}'

    def __eq__(self, other) -> bool:
        """
        Метод для сравнения объектов по зарплате.
        :param other: другой объект класса Vacancy
        :return: True, если зарплаты равны, иначе False
        """
        if isinstance(other, Vacancy):
            return (self.__salary['from'] == other.__salary['from']
                    and self.__salary['to'] == other.__salary['to'])
        else:
            raise TypeError('Неподдерживаемый тип операнда. Можно сравнить только объекты класса Vacancy.')

    def __lt__(self, other) -> bool:
        """
        Метод для сравнения объектов по зарплате.
        :param other: другой объект класса Vacancy
        :return: True, если зарплата меньше, иначе False
        """
        if isinstance(other, Vacancy):
            return (self.__salary['from'] < other.__salary['from']
                    and self.__salary['to'] < other.__salary['to'])
        else:
            raise TypeError('Неподдерживаемый тип операнда. Можно сравнить только объекты класса Vacancy.')

    def validate(self, rates: dict):
        """
        Метод для проверки корректности данных и приведения их к нужному формату.

        Например, если зарплата указана в USD или EUR, то переводит её в рубли.
        :return:
        """
        if self.__salary is None:
            self.__salary = {'from': 0, 'to': 0, 'currency': 'RUB'}
        elif self.__salary['to'] is None:
            self.__salary['to'] = 0

        if self.__salary['currency'] in rates:
            rate = rates[self.__salary['currency']]

            self.__salary['from'] *= rate
            self.__salary['to'] *= rate
            self.__salary['currency'] = 'RUB'
