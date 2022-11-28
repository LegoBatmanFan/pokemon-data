from enum import Enum


class Uri(str, Enum):
    US_WEATHER_URI = "https://api.weather.gov/points/"

    INTERNATIONAL_WEATHER_URI = "https://api.openweathermap.org/data/2.5/weather?"

    US_WEATHER_ALERTS_URI = "https://api.weather.gov/alerts/active?point="

    URI_QUERY_PARAMS = "&exclude=hourly,daily,minutely&units=imperial&appid="


class WeatherList:
    ORIGINAL_LIST = ['mostly sunny', 'rain showers', 'broken clouds', 'mostly cloudy', 'foggy mist', 'misty fog',
                     'partly sunny',
                     'clear', 'sunny', 'showers', 'overcast', 'clouds', 'winds', 'gusts', 'breeze', 'breezy',
                     'snow flurries', 'flurries', 'misty', 'foggy', 'mist', 'gust', 'rainfall', 'wind']

    NEW_LIST = ['sunny/clear', 'rain', 'partly cloudy', 'cloudy', 'fog', 'fog', 'sunny/clear',
                'sunny/clear', 'sunny/clear', 'rain', 'cloudy', 'cloudy', 'windy', 'windy', 'windy', 'windy',
                'snow', 'snow', 'fog', 'fog', 'fog', 'windy', 'rain', 'windy']

    POKE_TYPE_LIST = ['sunny/clear', 'rain', 'partly cloudy', 'cloudy', 'windy', 'snow', 'fog']


class HeaderInfo:
    USER_INFO = "<PROJECT_NAME>: <YOUR_EMAIL_ADDRESS>"
