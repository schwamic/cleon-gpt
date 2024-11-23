from agents.clients.weatherapi_client import WeatherAPIClient


def get_current_weather(city: str) -> str:
    """Calls a weather service and returns current weather data.

    Args:
        city: The location to get the weather for

    Returns:
        str: A description of the current weather in the specified city
    """
    client = WeatherAPIClient()
    data = client.get_current_weather(city)
    return str(data)
