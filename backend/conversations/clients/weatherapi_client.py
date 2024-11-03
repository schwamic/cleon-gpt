import requests
import os


class WeatherAPIClient():
    """
    A Client used to represent the interface for https://www.weatherapi.com/

    API Reference:
    https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2#/APIs/realtime-weather
    """

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.endpoint = os.getenv("WEATHER_ENDPOINT")

    def get_current_weather(self, city: str) -> str:
        call = f"{self.endpoint}/current.json?key={self.api_key}&q={city}"
        response = requests.get(call)
        return str(response.json())
