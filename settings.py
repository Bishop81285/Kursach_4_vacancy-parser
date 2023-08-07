from pathlib import Path

API_URL_HH = 'https://api.hh.ru/vacancies'
API_URL_SJ = 'https://api.superjob.ru/2.0/vacancies/'
API_URL_EXCH_RATES = 'https://api.apilayer.com/exchangerates_data/latest'

USE_LOCAL_DATA = True
ROOT_PATH = Path().resolve()
DATA_PATH = Path.joinpath(ROOT_PATH, 'data_json')

