import json
import os
import requests

from config import keys
from dotenv import load_dotenv


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote = quote.lower()
        base = base.lower()
        if quote == base:
            raise APIException("Невозможно перевести одинаковые валюты")

        try:
            quote_ticker = keys[quote]["ticker"]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.\n'
                               f'Вы можете ввести команду /values для вывода списка поддерживаемых валют')

        try:
            base_ticker = keys[base]["ticker"]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}\n'
                               f'Вы можете ввести команду /values для вывода списка поддерживаемых валют')

        try:
            amount = amount.replace(",", ".")
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}\n'
                               f'Количество представляет из себя целое либо дробное число.\n'
                               f'Для отделения дробной части можно применять как точку, так и запятую.')

        url = f'https://api.apilayer.com/exchangerates_data/convert' \
              f'?to={base_ticker}&from={quote_ticker}&amount={amount}'
        payload = {}
        load_dotenv()

        headers = {
            "apikey": os.getenv('API_KEY')
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        total = json.loads(response.content)['result']

        return total
