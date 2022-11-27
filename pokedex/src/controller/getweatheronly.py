from flask import Flask, jsonify
# from flask_restplus import Api, Resource
from flask_restx import Api, Resource
from src.service.weatherapi import WeatherApi
from src.service.weatherboost import WeatherBoost


class GetWeatherOnly(Resource):
    def get(self, lat, lon):
        my_weather = WeatherApi(lat, lon)
        data = my_weather.get_weather()

        return data