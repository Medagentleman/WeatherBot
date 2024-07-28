WeatherBot
Description
WeatherBot is a Telegram bot that provides current weather information for various cities in Russia. Users can select a city from a convenient list and instantly receive data about the current weather. The bot uses the OpenWeatherMap API to fetch data and the Telegram API for user interaction.

Technologies
Python: The primary programming language used to implement the bot.
python-telegram-bot: Library for interacting with the Telegram Bot API.
Requests: Library for making HTTP requests to the OpenWeatherMap API.
Logging: Module for logging bot activity and errors.
OpenWeatherMap API: External API for fetching current weather data.
Functionality
/start Command: Sends a welcome message and instructions on how to select a city.
/help Command: Displays a list of available commands and instructions.
/history Command: Shows the user's query history.
/stats Command: Provides statistics on the most requested cities.
Logging
Bot logs are saved in the bot.log file, which helps track all requests, errors, and user actions for easier debugging and monitoring.

Links
Telegram Bot API Documentation
OpenWeatherMap API Documentation
License
This project is licensed under the MIT License. See the LICENSE file for more details.
