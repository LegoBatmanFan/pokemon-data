from flask import Flask, jsonify
# from flask_restplus import Api, Resource
from flask_restx import Api, Resource
from src.controller.getweatheronly import GetWeatherOnly
from src.controller.getweatherandboost import GetWeatherAndBoost


flask_app = Flask(__name__)
api = Api(app=flask_app,
          version="1.0",
          title="Pokemon Predictor",
          description="Predict Pokemon spawns based on weather conditions at set of GPS coordinates")

api.add_resource(GetWeatherOnly, '/weather/<lat>,<lon>', endpoint='weather')
api.add_resource(GetWeatherAndBoost, '/weatherboost/<lat>,<lon>', endpoint='weatherboost')

# driver function
if __name__ == '__main__':
    flask_app.run(debug=True)