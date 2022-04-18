import requests
from  tokens_and_keys import *

keys = {'Евро': 'EUR',
'Юань': 'CNY',
'Рубль': 'RUB',
'Доллар': 'USD',
'Биткоин': 'BTC',
'Эфир': 'ETH'}



class APIException(Exception):
    pass

class CurrencyConverter:
    def __init__(self, base, quote, amount):
        self.base = base
        self.quote = quote
        self.amount = amount

    @staticmethod
    def get_price(base: str, quote:str, amount:str):
        if base == quote:
            raise APIException('Валюты одинаковые')


        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюты {base} нет в списке поддерживаемых валют')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюты {quote} нет в списке поддерживаемых валют')
        
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Неверно указано количествово')

        if amount <= 0:
            raise APIException('Количество не может быть меньше 0')


        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}&api_key={your_api_key}')
        data = response.json()
        total_base = data[keys[quote]] * amount
        
        return total_base