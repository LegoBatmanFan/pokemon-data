from flask import Flask, jsonify
# from flask_restplus import Api, Resource
from flask_restx import Api, Resource
from src.service.weatherapi import WeatherApi
from src.service.weatherboost import WeatherBoost


class GetWeatherAndBoost(Resource):
    def get(self, lat, lon):
        my_weather = WeatherApi(lat, lon)
        data = my_weather.get_weather()
        response = data[0]

        if response.get('forecast'):
            my_type = WeatherBoost(response)
            return jsonify(my_type.get_weather_boosts())
        else:
            return data
