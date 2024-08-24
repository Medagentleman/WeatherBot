import telebot
from telebot import types
import requests
import logging
import time

# Bot token
BOT_KEY = '00000000000000000000000000000000000'
# API key for OpenWeatherMap
OWM_API_KEY = '00000000000000000000000000000'
# Setting the token
bot = telebot.TeleBot(BOT_KEY)

bot = telebot.TeleBot(BOT_KEY)

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('bot.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Updated list of world capitals
WORLD_CITIES = [
    ["🌆 Moscow", "🏛️ Washington", "🌉 London"],
    ["🏯 Beijing", "🎎 Tokyo", "🕍 Berlin"],
    ["🗼 Paris", "🏛️ Rome", "🏰 Madrid"],
    ["🏙️ Ottawa", "🦘 Canberra", "🌳 Brasília"],
    ["🇮🇳 New Delhi", "🏞️ Buenos Aires", "🏜️ Cairo"],
    ["🌉 Ankara", "🌇 Riyadh", "🏜️ Tehran"],
    ["🏙️ Mexico City", "🌅 Pretoria", "🌄 Wellington"],
    ["🏙️ Seoul", "🏖️ Bangkok", "🏞️ Hanoi"],
    ["🏙️ Jakarta", "🌳 Nairobi", "🏛️ Baghdad"],
    ["🏙️ Dhaka", "🏛️ Athens", "🏞️ Helsinki"]
]

# Dictionary to store the last request time for each user
user_last_request_time = {}
user_warned_about_frequent_requests = {}
MIN_REQUEST_INTERVAL = 3  # Minimum time interval between requests in seconds

# Default settings
user_settings = {}

# Function to get weather in a specified city
def get_weather(city, units='metric', lang='en'):
    start_time = time.time()
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units={units}&lang={lang}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        duration = time.time() - start_time
        logger.info(f"Weather request for {city} completed in {duration:.2f} seconds")
        return f"Weather in {city}: {weather_description.capitalize()}, Temperature: {temperature}°{'C' if units == 'metric' else 'F'}"
    except (requests.exceptions.RequestException, KeyError) as e:
        duration = time.time() - start_time
        logger.error(f"Weather request for {city} failed in {duration:.2f} seconds: {e}")
        return f"Error getting weather: {e}"

# Function to create a keyboard with city buttons
def create_city_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for row in WORLD_CITIES:
        buttons = [types.KeyboardButton(city) for city in row]
        markup.add(*buttons)
    markup.add(types.KeyboardButton("⚙️ Settings"))
    return markup

# Function to create a settings keyboard
def create_settings_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton("🌐 Change Language"), types.KeyboardButton("🌡️ Change Temperature Units"))
    markup.add(types.KeyboardButton("🔙 Back"))
    return markup

# Function to create a language selection keyboard
def create_language_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton("English"), types.KeyboardButton("Русский"))
    markup.add(types.KeyboardButton("🔙 Back"))
    return markup

# Function to create a temperature units selection keyboard
def create_units_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton("Celsius"), types.KeyboardButton("Fahrenheit"))
    markup.add(types.KeyboardButton("🔙 Back"))
    return markup

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_info = f"User {message.from_user.id} ({message.from_user.username}) from {message.chat.id}, first_name: {message.from_user.first_name}, last_name: {message.from_user.last_name}"
    logger.info(f"{user_info} started the bot")
    bot.send_message(message.chat.id,
                     "Hello! I am a bot that can tell you the weather in various world capitals. Choose a city from the list below:",
                     reply_markup=create_city_keyboard())

# Handler for text messages and buttons
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    user_info = f"User {user_id} ({message.from_user.username}) from {message.chat.id}, first_name: {message.from_user.first_name}, last_name: {message.from_user.last_name}"

    current_time = time.time()
    last_request_time = user_last_request_time.get(user_id, 0)

    # Check if the user is making requests too frequently
    if current_time - last_request_time < MIN_REQUEST_INTERVAL:
        if not user_warned_about_frequent_requests.get(user_id, False):
            logger.warning(f"{user_info} is making requests too frequently")
            bot.send_message(message.chat.id, "Please wait a few seconds before requesting again.")
            user_warned_about_frequent_requests[user_id] = True
        return

    # Reset the warning if the user is making valid requests again
    user_warned_about_frequent_requests[user_id] = False

    # Check if the message is a command or a settings change
    if text == "⚙️ Settings":
        bot.send_message(message.chat.id, "Settings:", reply_markup=create_settings_keyboard())
    elif text == "🌐 Change Language":
        bot.send_message(message.chat.id, "Choose a language:", reply_markup=create_language_keyboard())
    elif text == "🌡️ Change Temperature Units":
        bot.send_message(message.chat.id, "Choose temperature units:", reply_markup=create_units_keyboard())
    elif text == "🔙 Back":
        bot.send_message(message.chat.id, "Back to main menu:", reply_markup=create_city_keyboard())
    elif text in ["English", "Русский"]:
        user_settings[user_id] = user_settings.get(user_id, {})
        user_settings[user_id]['lang'] = 'en' if text == "English" else 'ru'
        bot.send_message(message.chat.id, f"Language set to {text}.", reply_markup=create_settings_keyboard())
    elif text in ["Celsius", "Fahrenheit"]:
        user_settings[user_id] = user_settings.get(user_id, {})
        user_settings[user_id]['units'] = 'metric' if text == "Celsius" else 'imperial'
        bot.send_message(message.chat.id, f"Temperature units set to {text}.", reply_markup=create_settings_keyboard())
    elif any(text in row for row in WORLD_CITIES):
        logger.info(f"{user_info} requested weather for {text}")
        user_lang = user_settings.get(user_id, {}).get('lang', 'en')
        user_units = user_settings.get(user_id, {}).get('units', 'metric')
        weather = get_weather(text, units=user_units, lang=user_lang)
        bot.send_message(message.chat.id, weather)
        logger.info(f"{user_info} received weather info for {text}")
        user_last_request_time[user_id] = current_time  # Update the last request time
    else:
        logger.warning(f"{user_info} sent invalid message: {text}")
        bot.send_message(message.chat.id, "Choose a city from the list below:", reply_markup=create_city_keyboard())
        logger.info(f"{user_info} prompted to choose a city again")

# Start polling for messages
bot.polling(none_stop=True, interval=0)
