from flask import jsonify
from flask_restx import Resource
from src.service.weatherapi import WeatherApi
from src.service.weatherboost import WeatherBoost


class GetWeatherOnly(Resource):
    def get(self, lat, lon):
        return get_weather(lat, lon)


class GetWeatherAndBoost(Resource):
    def get(self, lat, lon):
        data = get_weather(lat, lon)
        response = data[0]
        return get_boost(data, response)


def get_weather(lat, lon):
    my_weather_api = WeatherApi(lat, lon)
    weather_response = my_weather_api.get_weather()
    return weather_response


def get_boost(data, response):
    if response.get('forecast'):
        my_type = WeatherBoost(response)
        return jsonify(my_type.get_weather_boosts())
    else:
        return data
