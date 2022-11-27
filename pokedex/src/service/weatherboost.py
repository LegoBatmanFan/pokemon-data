import re
import spacy
from spacy.matcher import PhraseMatcher
from src.constants.constants import WeatherList


class WeatherBoost:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_forecast(self):
        if self.weather_data.get('forecast').get('detailedForecast'):
            forecast_raw = self.weather_data.get('forecast').get('detailedForecast')
        elif self.weather_data.get('forecast').get('description'):
            forecast_raw = self.weather_data.get('forecast').get('description')
        elif self.weather_data.get('gen_forecast').get('description'):
            forecast_raw = self.weather_data.get('gen_forecast').get('description')
        else:
            forecast_raw = "ERROR"

        return forecast_raw

    @staticmethod
    def process_forecast(forecast_raw):
        forecast_processed = forecast_raw.lower()
        forecast_processed = re.sub('[^a-zA-Z]', ' ', forecast_processed)
        forecast_processed = re.sub(r'\s+', ' ', forecast_processed)

        for i in range(len(WeatherList.NEW_LIST)):
            forecast_processed = forecast_processed.replace(WeatherList.ORIGINAL_LIST[i], WeatherList.NEW_LIST[i])

        # Run this command to get the model:
        # python -m spacy download en_core_web_sm
        nlp = spacy.load('en_core_web_sm')
        boost_matcher = PhraseMatcher(nlp.vocab)
        WeatherList.POKE_TYPE_LIST = ['sunny/clear', 'rain', 'partly cloudy', 'cloudy', 'windy', 'snow', 'fog']

        boost_patterns = [nlp(text) for text in WeatherList.POKE_TYPE_LIST]
        boost_matcher.add('LH', None, *boost_patterns)
        boost_sentence = nlp(forecast_processed)
        matched_types = boost_matcher(boost_sentence)

        boost_types_list = []
        weather_boost_types = []
        for match_id, start, end in matched_types:
            rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
            span = boost_sentence[start: end]  # get the matched slice of the doc
            boost_types_list.append((rule_id, span.text))

        boost_set = set(boost_types_list)
        unique_boost_list = (list(boost_set))

        for i in range(len(unique_boost_list)):

            weather_boost_types.append(unique_boost_list[i][1])

        #https://www.geeksforgeeks.org/python-convert-a-list-to-dictionary/
        #pokemon_types_dct = {"types": {weather_boost_types[i]: weather_boost_types[i + 1] for i in range(0, len(weather_boost_types), 2)}}

        weather_boost_dct = dict({"boosts": weather_boost_types})

        return weather_boost_dct

    def get_weather_boosts(self):
        forecast_raw = self.get_forecast()
        boost_types = self.process_forecast(forecast_raw)

        weather_and_boosts_json = {**self.weather_data, **boost_types}

        return weather_and_boosts_json