from urllib import  parse, request
from configparser import ConfigParser

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

LANG = '&lang=es'

def _get_api_key():
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}&units={units}&appid={api_key}{LANG}"

    return url


def get_url_icon(icon_id:str):
    icon_id = icon_id
    BASE_ICON_URL = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    response = request.urlopen(BASE_ICON_URL)
    response.read()
    print (response.read())