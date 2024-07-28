# Weather Bot 🌤️

Welcome to the Weather Bot! This bot provides real-time weather updates for various world capitals. Just select a city from the list, and the bot will fetch the current weather information for you.

## Features

- **Real-time Weather Information**: Get the latest weather updates for world capitals.
- **User-friendly Interface**: Easy-to-use keyboard interface to select cities.
- **Logging**: Detailed logging of user interactions and weather requests.

## Technologies Used

- **Python**: The core programming language.
- **pyTelegramBotAPI**: A Python wrapper for the Telegram Bot API.
- **OpenWeatherMap API**: For fetching real-time weather data.
- **Logging**: For recording bot activities and user interactions.

## Setup and Installation

### Prerequisites

- Python 3.7+
- A Telegram Bot token from [BotFather](https://core.telegram.org/bots#botfather)
- An API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)

### Installation Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/weather-bot.git
    cd weather-bot
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure your tokens**:
   Update the `BOT_KEY` and `OWM_API_KEY` in the script with your Telegram Bot token and OpenWeatherMap API key, respectively.

### Running the Bot

Run the bot with the following command:
```sh
python weather_bot.py
