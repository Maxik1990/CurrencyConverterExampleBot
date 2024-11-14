# файл с классами для работы с API и исключениями
import requests
import json


class APIException(Exception):
    """Класс для пользовательских исключений"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        """Метод для получения цены валюты через API"""
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException("Ошибка при запросе к API.")

        data = response.json()

        if 'error' in data:
            raise APIException("Невалидный запрос, проверьте введенные валюты.")

        if quote not in data['rates']:
            raise APIException(f"Валюта {quote} не поддерживается.")

        rate = data['rates'][quote]
        total = rate * amount

        return total


class Currency:
    """Класс для работы с валютами, включает методы получения доступных валют."""

    @staticmethod
    def get_supported_currencies():
        """Возвращает список поддерживаемых валют"""
        return ['USD', 'EUR', 'RUB']