import json
import os

import requests

from settings import API_URL_EXCH_RATES

API_KEY: str = os.getenv('EXCHANGE_RATES_API_KEY')


def get_currency_rate(currency: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""

    url = API_URL_EXCH_RATES
    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': currency})
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]

    return rate
