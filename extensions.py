import json
import requests
from config import currency_keys

class Currency:
    api = 'http://api.exchangeratesapi.io/v1/latest?access_key=dc6be5790633985270dc0449a08ab3ba&symbols=USD,RUB&format=1'

    def __init__(self):
        self.r = requests.get(self.api)

    @staticmethod
    def check_data(quote, base, amount):
        if quote == base:
            raise APIException(f'Вы пытаетесь перевести {quote} в {base}')

        try:
            quote_tiker = currency_keys[quote]
        except KeyError:
            raise APIException(f'Не знаю такой валюты: {quote}')

        try:
            base_tiker = currency_keys[base]
        except KeyError:
            raise APIException(f'Не знаю такой валюты: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amount}')
        return quote, base, amount

    def get_price(self, base: str, quote: str, amount: str) -> float:
        rates = json.loads(self.r.content)['rates']
        rates['EUR'] = 1.0
        result = rates[currency_keys[quote]] / rates[currency_keys[base]] * float(amount)
        return result


class APIException(Exception):
    pass