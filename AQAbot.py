import os
import telebot
from telebot import types
import requests
import logging

# Получение токенов из переменных окружения
BOT_KEY = os.getenv('BOT_KEY', 'PUT_YOUR_BOT_TOKEN_HERE')
OWM_API_KEY = os.getenv('OWM_API_KEY', 'PUT_YOUR_API_TOKEN_HERE')

# Указываем токен
bot = telebot.TeleBot(BOT_KEY)

# Настройка логирования
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Список крупных городов России
RUSSIAN_CITIES = [
    ["Москва", "Мюнхен", "Нью-Йорк", "Мурманск"],
    ["Нижний Новгород", "Казань", "Челябинск", "Омск"],
    ["Самара", "Ростов-на-Дону", "Уфа", "Красноярск"],
    ["Пермь", "Воронеж", "Волгоград", "Краснодар"],
    ["Саратов", "Тюмень", "Тольятти", "Ижевск"]
]

# Получение погоды в указанном городе
def get_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=ru'
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Погода в городе {city}: {weather_description.capitalize()}, температура: {temperature}°C"
    except requests.exceptions.RequestException as e:
        return f"Ошибка сети: {e}"
    except KeyError as e:
        return f"Ошибка данных: {e}"

# Клавиатура для выбора города
def create_city_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for row in RUSSIAN_CITIES:
        buttons = [types.KeyboardButton(city.capitalize()) for city in row]
        markup.add(*buttons)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info(f"User {message.from_user.id} started the bot")
    bot.send_message(message.chat.id, "Привет! Я бот, который может сообщить тебе погоду в различных городах России. Выбери город из списка ниже:", reply_markup=create_city_keyboard())

# Обработчик текстовых сообщений и кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.capitalize()
    if any(text in row for row in RUSSIAN_CITIES):
        logging.info(f"User {message.from_user.id} requested weather for {text}")
        weather = get_weather(text)
        bot.send_message(message.chat.id, weather)
    else:
        logging.warning(f"User {message.from_user.id} sent invalid message")
        bot.send_message(message.chat.id, "Выбери город из списка ниже:", reply_markup=create_city_keyboard())

bot.polling(none_stop=True, interval=0)
