import telebot
from extensions import CurrencyConverter, Currency, APIException
import config

# Создаем экземпляр бота с использованием токена
bot = telebot.TeleBot(config.TOKEN)


# Команда /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "Привет! Для получения курса валют напишите в следующем формате:\n"
        "<валюта для конвертации> <валюта для получения> <количество>\n\n"
        "Например: EUR RUB 100\n\n"
        "Доступные валюты: USD, EUR, RUB\n\n"
        "Команда /values выводит список всех доступных валют."
    )


# Команда /values
@bot.message_handler(commands=['values'])
def send_values(message):
    currencies = Currency.get_supported_currencies()
    bot.send_message(message.chat.id, "Доступные валюты: " + ", ".join(currencies))


# Основной обработчик для запросов
@bot.message_handler(content_types=['text'])
def handle_conversion(message):
    try:
        # Разбираем сообщение на компоненты
        text = message.text.split()
        if len(text) != 3:
            raise APIException("Неправильный формат запроса. Используйте: <валюта_1> <валюта_2> <количество>")

        base, quote, amount = text[0].upper(), text[1].upper(), text[2]

        # Проверяем, что валюта корректна
        if base not in Currency.get_supported_currencies():
            raise APIException(f"Валюта {base} не поддерживается.")
        if quote not in Currency.get_supported_currencies():
            raise APIException(f"Валюта {quote} не поддерживается.")

        # Проверяем, что количество это число
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Количество должно быть числом, а не {amount}.")

        # Получаем цену
        total = CurrencyConverter.get_price(base, quote, amount)

        # Отправляем результат
        bot.send_message(message.chat.id, f"{amount} {base} = {total:.2f} {quote}")

    except APIException as e:
        # Обработка ошибок и вывод пользователю
        bot.send_message(message.chat.id, f"Ошибка: {e.message}")
    except Exception as e:
        # На случай других ошибок
        bot.send_message(message.chat.id, f"Произошла непредвиденная ошибка: {str(e)}")


# Запуск бота
bot.polling()