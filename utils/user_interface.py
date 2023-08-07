from time import sleep

from file_handler.json_handler import JsonHandler
from parser.hh import HhParser
from parser.sj import SjParser


def greet_user():
    """
    Функция для приветствия пользователя.
    :return: None
    """
    print("Привет, это программа для поиска и анализа вакансий с разных платформ.\n")
    print("Вы можете выбрать одну или несколько платформ для получения вакансий: hh.ru или superjob.ru.\n")


def get_platforms() -> list[str]:
    """
    Функция для получения списка платформ от пользователя.
    :return: список названий платформ
    """
    platforms = input("Введите названия платформ через запятую: ")
    platforms = platforms.split(",")

    return [platform.strip().lower() for platform in platforms]


def get_pages() -> int:
    """
    Функция для получения кол-ва страниц для обработки
    :return: кол-во страниц
    """
    vacancy_amount = int(input('Сколько вакансий вы хотите обработать? -> '))

    if vacancy_amount < 50 or vacancy_amount > 1000:
        sleep(2)
        print(f'Указано неверное кол-во вакансий: {vacancy_amount}. Диапазон: от 50 до 1000.\n')
        raise ValueError

    return vacancy_amount // 50


def get_vacancies(platforms: list, query: str, pages: int) -> list:
    """
    Функция для получения списка вакансий с выбранных платформ
    :param pages: кол-во страниц для обработки
    :param platforms: список выбранных платформ
    :param query: поисковой запрос пользователя
    :return: список вакансий
    """
    parsers = []

    for page in range(pages):
        for platform in platforms:
            if platform in ("hh.ru", 'hh'):
                parser = HhParser(query, page)
                parsers.append(parser)
            elif platform in ("superjob.ru", 'sj', 'superjob'):
                parser = SjParser(query, page)
                parsers.append(parser)
            else:
                sleep(2)
                print(f"Неверная платформа: {platform}.\n")
                raise ValueError

    vacancies = []

    for parser in parsers:
        vacancies.extend(parser.parse_data())

    return vacancies


def save_vacancies(vacancies: list) -> JsonHandler:
    """
    Функция для сохранения списка вакансий в файл
    :param vacancies: список объектов класса Vacancy
    :return: объект класса JsonHandler
    """
    file_handler = JsonHandler("vacancies.json")
    file_handler.add_vacancies(vacancies)

    print(f"В файл {file_handler.filename} сохранено {len(vacancies)} вакансий.\n")

    return file_handler


def show_options():
    """
    Функция для вывода списка возможных действий с данными
    :return: None
    """
    print("Вы можете выполнить следующие действия с данными:")
    print("1. Получить топ N вакансий по зарплате")
    print("2. Получить вакансии в отсортированном виде")
    print("3. Получить вакансии, в описании которых есть определенные ключевые слова")
    print("4. Удалить вакансии по какому-то критерию")
    print("5. Выйти из программы")


def get_action() -> str:
    """
    Функция для получения номера действия от пользователя
    :return: номер действия
    """
    action = input("Введите номер действия: ")

    if action not in ('1', '2', '3', '4', '5'):
        sleep(2)
        print(f'Неверно указан номер действия: {action}.\n')
        raise ValueError

    return action


def get_top_salary_vacancies(n: int, file_handler: JsonHandler):
    """
    Функция для вывода топ N вакансий по зарплате
    :param file_handler: объект для работы с файлом данных
    :param n: кол-во вакансий
    :return: None
    """
    top_vacancies = sorted(file_handler.get_vacancies(), key=lambda el: el.get_salary(), reverse=True)[:n]
    print(f"\nТоп {n} вакансий по зарплате:")

    for vacancy in top_vacancies:
        sleep(0.5)
        print(vacancy)
        print()


def get_sort_type() -> str:
    """
    Функция для возвращения типа сортировки
    :return: тип сортировки
    """
    print("Вы можете выбрать следующие варианты сортировки:")
    print("1. Сортировка по городам")
    print("2. Сортировка по зарплате")
    print("3. Сортировка по источнику вакансий (hh или sj)")

    while True:
        sort_type = input('Введите номер действия: ')

        if sort_type not in ('1', '2', '3'):
            sleep(1)
            print(f'Неверно указан номер действия: {sort_type}.\n')
            continue
        else:
            break

    return sort_type


def get_order_type() -> str:
    """
    Функция для возвращения порядка сортировки
    :return: порядок сортировки
    """
    while True:
        order = input("Введите порядок сортировки (asc - по возрастанию, desc - по убыванию): ")

        if order in ('asc', 'desc'):
            return order
        else:
            sleep(1)
            print(f"Неверный порядок сортировки: {order}.\n")
            continue


def show_sorted_vacancies(sorted_vacancies: list, sort_type: str, source: str = '', order: str = ''):
    """
    Функция для вывода отсортированных вакансий
    :param source: тип источника вакансии
    :param sort_type: тип сортировки
    :param order: порядок сортировки
    :param sorted_vacancies: список отсортированных вакансий
    :return:
    """
    count = 5

    if sort_type == '1':
        print(f"\nВакансии по городам в {order} порядке:")
    elif sort_type == '2':
        print(f"\nВакансии по зарплате в {order} порядке:")
    else:
        print(f"\nВакансии по источнику {source}:")

    while True:
        if count == len(sorted_vacancies):
            print("Вы просмотрели все отсортированные вакансии.\n")
            break

        for index, vacancy in enumerate(sorted_vacancies):
            if index == 5:
                break
            sleep(0.5)
            print(vacancy)
            print()

        print("Вы можете выбрать следующее:")
        print("1. Вывести еще 5 вакансий")
        print("2. Выйти из сортировки")

        while True:
            action = input('Введите номер действия: ')

            if action not in ('1', '2'):
                sleep(1)
                print(f'Неверно указан номер действия: {action}.\n')
                continue
            else:
                break

        if action == '1':
            count += 5
            continue
        else:
            print()
            break


def get_source_type() -> str:
    """
    Функция для возвращения типа источника
    :return: тип источника
    """
    while True:
        source = input("Введите тип источника для сортировки (hh или sj): ")

        if source in ('hh', 'sj'):
            return source
        else:
            sleep(1)
            print(f"Неверный тип источника: {source}.\n")
            continue


def get_keywords() -> dict:
    """
    Функция для получения критериев фильтрации
    :return: словарь ключевых слов
    """
    keywords = {}
    filters = ["city", "employer", "salary", "description", "requirements", "source"]

    print("\nВыберите какие фильтры вы хотите задать:")

    """print('1. Задать город для фильтрации')
    print('2. Задать фирму/компанию для фильтрации')
    print('3. Задать зарплату (мин и макс) для фильтрации')
    print('4. Задать ключевые слова для описания вакансии')
    print('5. Задать ключевые слова для требований вакансии')
    print('6. Задать источник вакансии (hh или superjob)')"""

    while filters:
        for i, filter_ in enumerate(filters, 1):
            print(f"{i}. Задать {filter_} для фильтрации")

        choice = int(input("Введите номер фильтра или 0, чтобы закончить: "))

        if choice == 0:
            break
        elif choice < 0 or choice > len(filters):
            sleep(1)
            print("Неверный номер, попробуйте еще раз.")
            continue
        else:
            filter_ = filters[choice - 1]

            if filter_ == "city":
                city = input("Введите название города: ")
                keywords["city"] = city

            elif filter_ == "employer":
                employer = input("Введите название работодателя: ")
                keywords["employer"] = employer

            elif filter_ == "salary":
                salary_from = int(input("Введите минимальную зарплату: "))
                salary_to = int(input("Введите максимальную зарплату: "))
                keywords["salary"] = {"from": salary_from, "to": salary_to}

            elif filter_ == "description":
                description = input("Введите ключевые слова для описания вакансии через запятую: ")
                description = description.split(",")
                description = [word.strip().lower() for word in description]

                keywords["description"] = description

            elif filter_ == "requirements":
                requirements = input("Введите ключевые слова для требований к кандидату через запятую: ")
                requirements = requirements.split(",")
                requirements = [word.strip().lower() for word in requirements]

                keywords["requirements"] = requirements

            elif filter_ == "source":
                source = input("Введите название источника вакансии (hh или sj): ")
                source = source.lower()
                keywords["source"] = source

            filters.remove(filter_)

            print(f'Выбранный фильтр {filter_} задан. Вы можете задать остальные фильтры: ост. {len(filters)}')

    print('\nВот ваш набор фильтров:')

    for key, value in keywords.items():
        print(f'Фильтр {key}: {value}')

    return keywords


def show_filtered_vacancies(filtered_vacancies):
    """
    Функция для вывода отфильтрованных вакансий
    :param filtered_vacancies: список отфильтрованных вакансий
    :return: None
    """
    count = 5

    while True:
        if count == len(filtered_vacancies):
            print("Вы просмотрели все вакансии по вашим фильтрам.\n")
            break

        for index, vacancy in enumerate(filtered_vacancies):
            if index == 5:
                break

            sleep(0.5)
            print(vacancy)
            print()

        print("Вы можете выбрать следующее:")
        print("1. Вывести еще 5 вакансий")
        print("2. Выйти из просмотра")

        while True:
            action = input('Введите номер действия: ')

            if action not in ('1', '2'):
                sleep(1)
                print(f'Неверно указан номер действия: {action}.\n')
                continue
            else:
                break

        if action == '1':
            count += 5
            continue
        else:
            print()
            break


def keywords_confirmation(keywords) -> dict:
    """
    Функция для получения подтвержденных критериев для удаления вакансий
    :param keywords: пользовательские фильтры
    :return: словарь подтвержденных ключевых слов
    """
    confirmed_keywords = {}

    for key, value in keywords.items():
        while True:
            confirm = input(f"Вы действительно хотите удалить все вакансии с {key} {value}? (да/нет): ")
            confirm = confirm.lower()

            if confirm == "да":
                confirmed_keywords[key] = value
                break
            elif confirm == "нет":
                print(f"Тогда мы не будем учитывать {key} при удалении.")
                break
            else:
                print("Неверный ответ, попробуйте еще раз.")
                continue

    return confirmed_keywords


def perform_action(action: str, file_handler: JsonHandler):
    """
    Функция для выполнения выбранного действия с данными
    :param action: выбранное пользователем действие (1-5)
    :param file_handler: объект для работы с файлом данных
    :return: None
    """
    if action == '1':
        n = int(input("Введите количество вакансий: "))

        if not 0 < n < len(file_handler):
            sleep(2)
            print(f'Неверное кол-во вакансий: {n}. Допустимый диапазон: от 1 до {len(file_handler)}.\n')
            raise ValueError

        get_top_salary_vacancies(n, file_handler)

    elif action == '2':
        sort_type = get_sort_type()

        if sort_type == '1':
            order = get_order_type()

            if order == "asc":
                sorted_vacancies_city = sorted(file_handler.get_vacancies(), key=lambda el: el.location)
            else:
                sorted_vacancies_city = sorted(file_handler.get_vacancies(), key=lambda el: el.location,
                                               reverse=True)

            show_sorted_vacancies(sorted_vacancies_city, sort_type, order=order)

        elif sort_type == '2':
            order = get_order_type()

            if order == "asc":
                sorted_vacancies_salary = sorted(file_handler.get_vacancies(), key=lambda el: el.get_salary())
            else:
                sorted_vacancies_salary = sorted(file_handler.get_vacancies(), key=lambda el: el.get_salary(),
                                                 reverse=True)

            show_sorted_vacancies(sorted_vacancies_salary, sort_type, order=order)
        else:
            source = get_source_type()

            if source == 'hh':
                vacancies = file_handler.get_vacancies()
                sorted_vacancies_source = [el for el in vacancies if el.source == 'hh.ru']
            else:
                vacancies = file_handler.get_vacancies()
                sorted_vacancies_source = [el for el in vacancies if el.source == 'superjob.ru']

            show_sorted_vacancies(sorted_vacancies_source, sort_type, source=source)

    elif action == '3':
        keywords = get_keywords()

        filtered_vacancies = file_handler.get_vacancies(**keywords)

        print(f"\nВакансии, в описании которых есть выбранные фильтры:")

        show_filtered_vacancies(filtered_vacancies)

    elif action == '4':
        keywords = get_keywords()

        confirmed_keywords = keywords_confirmation(keywords)

        vacancies_to_delete = file_handler.get_vacancies(**confirmed_keywords)

        file_handler.delete_vacancies(vacancies_to_delete)
        print(f"Из файла {file_handler.filename} удалено {len(vacancies_to_delete)} вакансий.")


def interact() -> int:
    """
    Функция для взаимодействия с пользователем через консоль.
    :return: None
    """
    greet_user()

    platforms = get_platforms()
    query = input("Введите поисковый запрос: ")

    try:
        pages = get_pages()
        vacancies = get_vacancies(platforms, query, pages)
    except ValueError:
        print('Ошибка при обработке запроса. Попробуйте еще раз.\n')
        sleep(2)
        return 1

    file_handler = save_vacancies(vacancies)

    show_options()

    try:
        action = get_action()
    except ValueError:
        print('Ошибка при обработке запроса. Попробуйте еще раз.\n')
        sleep(2)
        return 1

    while action != "5":
        try:
            perform_action(action, file_handler)

            show_options()

            action = get_action()
        except ValueError:
            print('Ошибка при обработке запроса. Попробуйте еще раз.\n')
            sleep(2)
            return 1

    return 0
