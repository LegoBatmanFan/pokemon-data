import requests
import json
from src.constants.constants import Uri
from src.constants.constants import HeaderInfo
from src.keys.keys import KeyConstants
from flask import Response
from flask import jsonify, make_response


class WeatherApi:

    def __init__(self, latitude, longitude):
        self.latitude = str(latitude)
        self.longitude = str(longitude)
        self.headers = {"Connection": "keep-alive", "User-Agent": HeaderInfo.USER_INFO}
        self.international_uri = Uri.INTERNATIONAL_WEATHER_URI + "lat=" + self.latitude + "&lon=" + self.longitude + Uri.URI_QUERY_PARAMS + KeyConstants.APK_KEY

    def get_weather(self):
        weather_api_response = self.get_data_from_weather_dot_gov(
            Uri.US_WEATHER_URI + self.latitude + "," + self.longitude)
        if weather_api_response[1].status_code == 200 and weather_api_response[0].get('properties'):

            location_key = "location"
            gen_forecast_key = "gen_forecast"
            forecast_key = "forecast"
            alert_key = "alert"

            # Get the city and state
            my_location = self.get_city_state_timezone(weather_api_response)

            # Get some general info about the location
            my_gen_forecast = self.get_general_forecast_info(self.international_uri)

            # Check to see if the forecast field is not null. If it's null, print a message saying the forecast is
            # not available
            my_detailed_forecast = self.get_forecast(weather_api_response)

            # Check for a weather alert
            my_alerts = self.check_for_alert(Uri.US_WEATHER_ALERTS_URI + self.latitude + "," + self.longitude)

            final_weather_json = {location_key: my_location,
                                  gen_forecast_key: my_gen_forecast,
                                  forecast_key: my_detailed_forecast,
                                  alert_key: my_alerts}
            my_status_code = 200
        # If the GPS coordinates are not in the US, you'll get a 404 code and the message "Data Unavailable For
        # Requested Point"
        # This means we need to check a different API
        elif weather_api_response[1].status_code == 404 and weather_api_response[0].get(
                'title') == "Data Unavailable For Requested Point":
            final_weather_json = self.get_weather_for_international_location(weather_api_response,
                                                                             self.international_uri)
            my_status_code = 200
        # For all other status codes, print the status code and message (detail field)
        else:
            my_status_code = weather_api_response[1].status_code
            status_code_key = "status_code"
            error_msg = "error"

            final_weather_json = {status_code_key: weather_api_response[1].status_code,
                                  error_msg: weather_api_response[0].get('detail'),
                                  "detail": "Invalid input: ",
                                  "latitude": self.latitude,
                                  "longitude": self.longitude}

        return final_weather_json, my_status_code

    def get_data_from_weather_dot_gov(self, my_url):
        my_response = requests.request("GET", my_url, headers=self.headers)

        # Create Python object from JSON string data
        my_response_obj = json.loads(my_response.text)
        return [my_response_obj, my_response]

    @staticmethod
    def get_data_from_open_weather_map(my_url):
        my_response = requests.request("GET", my_url)

        # Create Python object from JSON string data
        my_response_obj = json.loads(my_response.text)
        return [my_response_obj, my_response]

    @staticmethod
    def get_city_state_timezone(my_response):
        # Get the city and state
        my_city = str(my_response[0].get('properties').get('relativeLocation').get('properties').get('city'))
        my_state = str(my_response[0].get('properties').get('relativeLocation').get('properties').get('state'))
        my_timezone = str(my_response[0].get('properties').get('timeZone'))
        city = "city"
        state = "state"
        time_zone = "time_zone"

        city_json = {city: my_city,
                     state: my_state,
                     time_zone: my_timezone}
        return city_json

    def get_general_forecast_info(self, my_url):
        general_info_response = self.get_data_from_open_weather_map(my_url)

        main_key = "src"
        description_key = "description"
        temp_key = "temp"
        error_key = "error"
        error_msg = "DATA NOT AVAILABLE"

        if general_info_response[1].status_code == 200 and general_info_response[0].get('weather')[0]:
            gen_forecast_json = {
                description_key: str(
                    general_info_response[0].get('weather')[0].get('description')),
                temp_key: str(general_info_response[0].get('main').get('temp'))}
        else:
            gen_forecast_json = {error_key: error_msg}

        return gen_forecast_json

    def get_forecast(self, my_response):
        forecast_fields = ["name", "isDaytime", "temperature", "temperatureUnit", "windSpeed", "windDirection",
                           "shortForecast", "detailedForecast"]
        forecast_not_available_key = "forecast_not_available"
        forecast_not_available_msg = "FORECAST IS NOT AVAILABLE"
        forecast_link_key = "forecast_link"
        forecast_link_msg = "FORECAST LINK IS NOT AVAILABLE"

        if my_response[0].get('properties').get('forecast'):

            forecast_url = my_response[0].get('properties').get('forecast')

            forecast_response = self.get_data_from_weather_dot_gov(forecast_url)

            if forecast_response[1].status_code == 200 and forecast_response[0].get('properties'):
                detailed_forecast_json = {forecast_fields[0]: str(
                    forecast_response[0].get('properties').get('periods')[0].get(forecast_fields[0])),
                    forecast_fields[1]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[1])),
                    forecast_fields[2]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[2])),
                    forecast_fields[3]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[3])),
                    forecast_fields[4]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[4])),
                    forecast_fields[5]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[5])),
                    forecast_fields[6]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[6])),
                    forecast_fields[7]: str(
                        forecast_response[0].get('properties').get('periods')[0].get(
                            forecast_fields[7]))}
            else:
                detailed_forecast_json = {forecast_not_available_key: forecast_not_available_msg}

        else:
            detailed_forecast_json = {forecast_link_key: forecast_link_msg}

        return detailed_forecast_json

    def check_for_alert(self, my_alerts_url):
        # Check for a weather alert
        # Look at this website: https://www.accuweather.com/en/us/severe-weather

        no_alerts_key = "no_alerts"
        no_alerts_msg = "There are no alerts"
        alerts_error_key = "alerts_error"
        alerts_error_msg = "alerts are not available at this time"

        alert_fields = ["areaDesc", "effective", "onset", "expires", "onset", "ends", "severity", "headline",
                        "description"]
        alert_response = self.get_data_from_weather_dot_gov(my_alerts_url)

        if alert_response[1].status_code == 200:

            # The features field (list) contains the alert info. If there is no alert, this list has a length of zero
            if len(alert_response[0].get("features")) == 0:
                alert_json = {no_alerts_key: no_alerts_msg}
            else:
                # Print the fields in the alert_fields_list structure

                alert_json = {
                    alert_fields[0]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[0])),
                    alert_fields[1]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[1])),
                    alert_fields[2]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[2])),
                    alert_fields[3]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[3])),
                    alert_fields[4]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[4])),
                    alert_fields[5]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[5])),
                    alert_fields[6]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[6])),
                    alert_fields[7]: str(
                        alert_response[0].get('features')[0].get('properties').get(alert_fields[7])), }
        else:
            # For all other status codes, just say alerts are not available at this time.
            alert_json = {alerts_error_key: alerts_error_msg}

        return alert_json

    def get_weather_for_international_location(self, my_response, my_url):
        intl_keys = ["name", "dt", "description", "temp", "feels_like", "humidity", "wind_speed", "country"]

        error_msg_key = "message"
        error_msg = "ERROR"
        location_key = "location"
        gen_forecast_key = "gen_forcast"
        forecast_key = "forecast"

        no_data_msg_key = "no_data_message"
        check_intnat_api_msg_key = "check_int_api_msg"
        intnat_api_info_key = "intnat_api_info"

        check_intnat_api_msg = "Checking the international weather api..."

        international_response = self.get_data_from_open_weather_map(my_url)

        if international_response[1].status_code == 200 and international_response[0].get('weather')[0]:
            intnatl_json = {intnat_api_info_key: {no_data_msg_key: my_response[0].get('detail'),
                                                  check_intnat_api_msg_key: check_intnat_api_msg},
                            location_key: {intl_keys[0]: str(international_response[0].get(intl_keys[0])),
                                           intl_keys[1]: str(international_response[0].get(intl_keys[1])),
                                           intl_keys[7]: str(international_response[0].get("sys").get(intl_keys[7]))},
                            gen_forecast_key: {intl_keys[2]: str(
                                international_response[0].get('weather')[0].get(intl_keys[2])),
                                intl_keys[3]: str(
                                    international_response[0].get('main').get(
                                        intl_keys[3])),
                                intl_keys[4]: str(
                                    international_response[0].get(intl_keys[4]))},
                            forecast_key: {
                                intl_keys[4]: str(international_response[0].get('main').get(intl_keys[4])),
                                intl_keys[5]: str(international_response[0].get(intl_keys[5])),
                                intl_keys[6]: str(international_response[0].get(intl_keys[6])),
                                intl_keys[2]: str(international_response[0].get('weather')[0].get(
                                    intl_keys[2])),
                                intl_keys[3]: str(
                                    international_response[0].get('weather')[0].get(intl_keys[3]))
                            }}

        else:
            intnatl_json = {error_msg_key: error_msg,
                            "status_code": international_response[1].status_code}

        return intnatl_json
