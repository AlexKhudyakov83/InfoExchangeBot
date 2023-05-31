import requests
import json
from currency import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'{quote} - одинаковые валюты')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'{quote} - не верный ввод')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'{base} - не верный ввод')
        try:
            amount = float(amount)
        except KeyError:
            raise ConvertionException(f'{amount} - не верный ввод')
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]
        return total_base * amount
