import requests
from config import WEATHER_API_KEY
from datetime import datetime


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code != 200:
        return "Не удалось получить данные о погоде. Проверьте название города."

    data = response.json()

    city_name = data['name']
    description = data['weather'][0]['description'].capitalize()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')

    weather_info = (
        f"<b>Погода в {city_name}</b>\n\n"
        f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"Описание: {description}\n"
        f"Влажность: {humidity}%\n"
        f"Ветер: {wind_speed} м/с\n"
        f"Восход: {sunrise}\n"
        f"Закат: {sunset}"
    )

    return weather_info