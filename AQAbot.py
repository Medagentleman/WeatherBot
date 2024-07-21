import telebot
from telebot import types
import requests
import logging


# Токен бота
BOT_Key = 'токен, сгенерированный при помощи @https://t.me/BotFather'
# API ключ для OpenWeatherMap
OWM_API_KEY = 'токен, полученный openweathermap.org '
# Указываем токен
bot = telebot.TeleBot(BOT_Key)

# Настройка логирования
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# Список крупных городов России
RUSSIAN_CITIES = [
    ["Москва", "Мюнхен", "Нью-Йорк", "МУРМАНСК"],
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
    except (requests.exceptions.RequestException, KeyError) as e:
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
    logging.info(f"User {message.from_user.id} started the bot")
    bot.send_message(message.chat.id, "Привет! Я бот, который может сообщить тебе погоду в различных городах России. Выбери город из списка ниже:", reply_markup=create_city_keyboard())

# Обработчик текстовых сообщений и кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if any(text in row for row in RUSSIAN_CITIES):
        logging.info(f"User {message.from_user.id} requested weather for {text}")
        weather = get_weather(text)
        bot.send_message(message.chat.id, weather)
    else:
        logging.warning(f"User {message.from_user.id} sent invalid message")
        bot.send_message(message.chat.id, "Выбери город из списка ниже:", reply_markup=create_city_keyboard())

# Обработчик входящих текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    logging.info(f"User {message.from_user.id} sent message: {message.text}")
    bot.send_message(message.chat.id, "Извините, я не понимаю вашего сообщения. Пожалуйста, выберите город из списка ниже:", reply_markup=create_city_keyboard())



bot.polling(none_stop=True, interval=0)


















# # Импортируем типы из модуля, чтобы создавать кнопки
# from telebot import types
# # Заготовки для трёх предложений
# first = ["Сегодня — идеальный день для новых начинаний.","Оптимальный день для того, чтобы решиться на смелый поступок!","Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.","Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.","Плодотворный день для того, чтобы разобраться с накопившимися делами."]
# second = ["Но помните, что даже в этом случае нужно не забывать про","Если поедете за город, заранее подумайте про","Те, кто сегодня нацелен выполнить множество дел, должны помнить про","Если у вас упадок сил, обратите внимание на","Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
# second_add = ["отношения с друзьями и близкими.","работу и деловые вопросы, которые могут так некстати помешать планам.","себя и своё здоровье, иначе к вечеру возможен полный раздрай.","бытовые вопросы — особенно те, которые вы не доделали вчера.","отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
# third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.","Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.","Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.","Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.","Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]
# # Метод, который получает сообщения и обрабатывает их
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     # Если написали «Привет»
#     if message.text == f"Привет":
#         # Пишем приветствие
#         bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
#         # Готовим кнопки
#         keyboard = types.InlineKeyboardMarkup()
#         # По очереди готовим текст и обработчик для каждого знака зодиака
#         key_knopka = types.InlineKeyboardButton(text='НАЖМИ ДЛЯ НАЧАЛА РАБОТЫ', callback_data='prikol')
#         keyboard.add(key_knopka)
#         key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
#         # И добавляем кнопку на экран
#         keyboard.add(key_oven)
#         key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
#         keyboard.add(key_telec)
#         key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
#         keyboard.add(key_bliznecy)
#         key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
#         keyboard.add(key_rak)
#         key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
#         keyboard.add(key_lev)
#         key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
#         keyboard.add(key_deva)
#         key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
#         keyboard.add(key_vesy)
#         key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
#         keyboard.add(key_scorpion)
#         key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
#         keyboard.add(key_strelec)
#         key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
#         keyboard.add(key_kozerog)
#         key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
#         keyboard.add(key_vodoley)
#         key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
#         keyboard.add(key_ryby)
#         # Показываем все кнопки сразу и пишем сообщение о выборе
#         bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши Привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Привет.")
# # Обработчик нажатий на кнопки
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     # Если нажали на одну из 12 кнопок — выводим гороскоп
#     if call.data == "zodiac":
#         # Формируем гороскоп
#         msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)
#         # Отправляем текст в Телеграм
#         bot.send_message(call.message.chat.id, msg)
#          # Если нажали на РЕКЛАМНУЮ КНОПКУ — выводим рекламу
#     elif call.data == "prikol":
#         #Здесь прописываем рекламное сообщение
#         msg = '++++++++++++++Здесь могла быть Ваша реклама++++++++++++++Теперь выберите знак зодиака'
#         # Отправляем текст в Телеграм
#         bot.send_message(call.message.chat.id, msg)
#
# # Запускаем постоянный опрос бота в Телеграме
# bot.polling(none_stop=True, interval=0)










