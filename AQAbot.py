import os
import telebot
import logging
import requests
from telebot import types

# Получение токенов из переменных окружения
BOT_KEY = os.getenv('BOT_KEY', 'bot token from Telegram APP')
OWM_API_KEY = os.getenv('OWM_API_KEY', 'API from weather resourse')

# Указываем токен
bot = telebot.TeleBot(BOT_KEY)

# Настройка логирования
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'  # Добавлена кодировка utf-8
)
logger = logging.getLogger(__name__)

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
    logger.info(f"Attempting to get weather for city: {city}")
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=ru'
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        logger.info(f"Successfully got weather for city: {city}")
        return f"Погода в городе {city}: {weather_description.capitalize()}, температура: {temperature}°C"
    except (requests.exceptions.RequestException, KeyError) as e:
        logger.error(f"Error getting weather for city {city}: {e}")
        return f"Ошибка при получении погоды: {e}"

# Клавиатура для выбора города
def create_city_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for row in RUSSIAN_CITIES:
        buttons = [types.KeyboardButton(city) for city in row]
        markup.add(*buttons)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который может сообщить тебе погоду в различных городах России. Выбери город из списка ниже:",
        reply_markup=create_city_keyboard()
    )

# Обработчик текстовых сообщений и кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user
    text = message.text
    logger.info(f"User {user.id} ({user.username}) sent message: {text}")

    if any(text in row for row in RUSSIAN_CITIES):
        logger.info(f"User {user.id} ({user.username}) requested weather for {text}")
        weather = get_weather(text)
        bot.send_message(message.chat.id, weather)
    else:
        logger.warning(f"User {user.id} ({user.username}) sent invalid message")
        bot.send_message(
            message.chat.id,
            "Выбери город из списка ниже:",
            reply_markup=create_city_keyboard()
        )

# Обработчик входящих текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user = message.from_user
    logger.info(f"User {user.id} ({user.username}) sent unrecognized message: {message.text}")
    bot.send_message(
        message.chat.id,
        "Извините, я не понимаю вашего сообщения. Пожалуйста, выберите город из списка ниже:",
        reply_markup=create_city_keyboard()
    )

bot.polling(none_stop=True, interval=0)
