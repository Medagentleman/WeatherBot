import telebot
from telebot import types
import requests
import logging
import time

# Bot token
BOT_KEY = '01234567890'
# API key for OpenWeatherMap
OWM_API_KEY = '01234567890'
# Setting the token
bot = telebot.TeleBot(BOT_KEY)

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File handler for logging
file_handler = logging.FileHandler('bot.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler for logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Updated list of world capitals
WORLD_CITIES = [
    ["Moscow", "Washington", "London"],
    ["Beijing", "Tokyo", "Berlin"],
    ["Paris", "Rome", "Madrid"],
    ["Ottawa", "Canberra", "Brasília"],
    ["New Delhi", "Buenos Aires", "Cairo"],
    ["Ankara", "Riyadh", "Tehran"],
    ["Mexico City", "Pretoria", "Wellington"],
    ["Seoul", "Bangkok", "Hanoi"],
    ["Jakarta", "Nairobi", "Baghdad"],
    ["Dhaka", "Athens", "Helsinki"]
]

# Function to get weather in a specified city
def get_weather(city):
    start_time = time.time()  # Record the start time
    try:
        # API request to OpenWeatherMap
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=en'
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        duration = time.time() - start_time  # Calculate the request duration
        logger.info(f"Weather request for {city} completed in {duration:.2f} seconds")
        return f"Weather in {city}: {weather_description.capitalize()}, Temperature: {temperature}°C"
    except (requests.exceptions.RequestException, KeyError) as e:
        duration = time.time() - start_time  # Calculate the request duration in case of error
        logger.error(f"Weather request for {city} failed in {duration:.2f} seconds: {e}")
        return f"Error getting weather: {e}"

# Function to create a keyboard with city buttons
def create_city_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for row in WORLD_CITIES:
        buttons = [types.KeyboardButton(city) for city in row]
        markup.add(*buttons)
    return markup

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_info = f"User {message.from_user.id} ({message.from_user.username}) from {message.chat.id}, first_name: {message.from_user.first_name}, last_name: {message.from_user.last_name}"
    logger.info(f"{user_info} started the bot")
    bot.send_message(message.chat.id,
                     f"Hello, {message.from_user.first_name}! I'm here to help you find the weather in various world capitals. Please choose a city from the list below:",
                     reply_markup=create_city_keyboard())

# Handler for all types of messages
@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_message(message):
    user_info = f"User {message.from_user.id} ({message.from_user.username}) from {message.chat.id}, first_name: {message.from_user.first_name}, last_name: {message.from_user.last_name}"

    if message.content_type == 'text':
        text = message.text
        logger.info(f"{user_info} sent text message: {text}")

        # Check if the message text matches any city in the list
        if any(text in row for row in WORLD_CITIES):
            logger.info(f"{user_info} requested weather for {text}")
            weather = get_weather(text)
            bot.send_message(message.chat.id, weather)
            logger.info(f"{user_info} received weather info for {text}")
        else:
            logger.warning(f"{user_info} sent invalid message: {text}")
            bot.send_message(message.chat.id, f"Hi again, {message.from_user.first_name}! Please choose a city from the list below:", reply_markup=create_city_keyboard())
            logger.info(f"{user_info} prompted to choose a city again")

    elif message.content_type == 'photo':
        logger.info(f"{user_info} sent photo")
        bot.send_message(message.chat.id, "Nice photo! But I can only tell you the weather.")

    elif message.content_type == 'video':
        logger.info(f"{user_info} sent video")
        bot.send_message(message.chat.id, "Interesting video! But let's talk about the weather instead.")

# Start polling for messages
bot.polling(none_stop=True, interval=0)
