from urllib import  parse, request, error
from configparser import ConfigParser
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from tkinter import ttk


def read_user_cli_args():
    """ Handles the CLI user interactions.
    
    Returns:
        argparse.Namespace: Populated namespace object"""

    parser = argparse.ArgumentParser (
        description="gets weather and temperature information for a city"
    )

    parser.add_argument("city", nargs="+", type=str, help="enter the city name")
    parser.add_argument("-i", "--imperial", action = "store_true", help="display the temperature in imperial units")
    return parser.parse_args()


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

# weather.py




def get_weather_json(query_url):
    """Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint

    Returns:
        dict: Weather information for a specific city
    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: #401 unauthorized
            sys.exit("Access denied. Check your api key")
        elif http_error.code == 404: #404 Not found
            sys.exit("Can't find weather data for this city")
        else:
            sys.exit(f"Something went wrong...({http_error})")
    
    data = response.read()
    
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("couldn't read server response")


def get_weather_data (weather_json):
    """ get only data without mixture or manipulation"""
    
    city = weather_json["name"]
    country = weather_json["sys"]["country"]
    location = f"{city}, {country}"
    
    weather_id = weather_json["weather"][0]["id"]
    weather_description = weather_json["weather"][0]["description"]
    weather_icon = weather_json["weather"][0]["icon"]
    temperature = weather_json["main"]["temp"]
    feels_like = weather_json["main"]["feels_like"]
    wind_speed = weather_json["wind"]["speed"]

    
    #wind_json = open_wind_class_data ('classification_wind.json')
    #wind_info = wind_classifier(wind_speed, wind_json)
    
    current_time = datetime.now()
    uct_time = datetime.now(timezone.utc)
    
    current_local_time =  uct_time + timedelta(seconds= weather_json["timezone"])
    
    current_time = datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')
    #current_local_time = datetime.strftime(current_local_time, '%Y-%m-%d %H:%M:%S')
    meassure_dt = weather_json["dt"]

    data_dic = {"location":location,
                "weather_id":weather_id,
                "weather_description":weather_description,
                "weather_icon":weather_icon,
                "temperature":temperature,
                "feels_like":feels_like,
                "wind_speed":wind_speed,
                "current_time":current_time,
                "current_local_time":current_local_time,
                "meassure_dt":meassure_dt
                }

    return data_dic



def open_wind_class_data(filename:str):
    with open(filename, encoding='utf-8') as f:
        wind_dict = json.load(f)
        return wind_dict


def wind_classifier(wind_speed:int, wind_dict:dict):
    wind_speed = int(wind_speed * (3600/1000))
    match wind_speed:
        case _ as speed if speed > 0 and speed <= wind_dict['CALMA']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['CALMA']['short_desc']}"
            wind_long_desc = f"{wind_dict['CALMA']['long_desc']}"
        case _ as speed if speed > wind_dict['CALMA']['speed'] and speed <= wind_dict['BRISA']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['BRISA']['short_desc']}"
            wind_long_desc = f"{wind_dict['BRISA']['long_desc']}"
        case _ as speed if speed > wind_dict['BRISA']['speed'] and speed <= wind_dict['VIENTO_LEVE']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['VIENTO_LEVE']['short_desc']}"
            wind_long_desc = f"{wind_dict['VIENTO_LEVE']['long_desc']}"
        case _ as speed if speed > wind_dict['VIENTO_LEVE']['speed'] and speed <= wind_dict['VIENTO_MODERADO']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['VIENTO_MODERADO']['short_desc']}"
            wind_long_desc = f"{wind_dict['VIENTO_MODERADO']['long_desc']}"
        case _ as speed if speed > wind_dict['VIENTO_MODERADO']['speed'] and speed <= wind_dict['VIENTO_REGULAR']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['VIENTO_REGULAR']['short_desc']}"
            wind_long_desc = f"{wind_dict['VIENTO_REGULAR']['long_desc']}"
        case _ as speed if speed > wind_dict['VIENTO_REGULAR']['speed'] and speed <= wind_dict['VIENTO_FUERTE']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['VIENTO_FUERTE']['short_desc']}"
            wind_long_desc = f"{wind_dict['VIENTO_FUERTE']['long_desc']}"
        case _ as speed if speed > wind_dict['VIENTO_FUERTE']['speed'] and speed <= wind_dict['VIENTO_MUY_FUERTE']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['VIENTO_MUY_FUERTE']['short_desc']}"
            wind_long_desc = f"{wind_dict['VIENTO_MUY_FUERTE']['long_desc']}"
        case _ as speed if speed > wind_dict['VIENTO_MUY_FUERTE']['speed'] and speed <= wind_dict['TEMPORAL']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['TEMPORAL']['short_desc']}"
            wind_long_desc = f"{wind_dict['TEMPORAL']['long_desc']}"
        case _ as speed if speed > wind_dict['TEMPORAL']['speed'] and speed <= wind_dict['TEMPORAL_FUERTE']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['TEMPORAL_FUERTE']['short_desc']}"
            wind_long_desc = f"{wind_dict['TEMPORAL_FUERTE']['long_desc']}"
        case _ as speed if speed > wind_dict['TEMPORAL_FUERTE']['speed'] and speed <= wind_dict['TORMENTA']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['TORMENTA']['short_desc']}"
            wind_long_desc = f"{wind_dict['TORMENTA']['long_desc']}"
        case _ as speed if speed > wind_dict['TORMENTA']['speed'] and speed <= wind_dict['TORMENTA_VIOLENTA']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['TORMENTA_VIOLENTA']['short_desc']}"
            wind_long_desc = f"{wind_dict['TORMENTA_VIOLENTA']['long_desc']}"
        case _ as speed if speed >= wind_dict['HURACAN']['speed']:
            wind_short_desc = f"{wind_speed}km/h: {wind_dict['HURACAN']['short_desc']}"
            wind_long_desc = f"{wind_dict['HURACAN']['long_dsc']}"
    return wind_short_desc, wind_long_desc


def build_weather_data_set(data_dic):
    """ Built data set to display on the screen"""
    wind_json = open_wind_class_data ('classification_wind.json')
    wind_info = wind_classifier(data_dic["wind_speed"], wind_json)
    data_dic['wind_speed'] = wind_info
    return (data_dic)

def get_city_entry():
    city = city_entry.get()
    return (city)

def flat_weather_dict (weather:dict):
    weather_str = str()
    for key, value in weather.items():
        weather_str += key + ": " + value + "\t"
    return (weather_str)


def display_on_windows(weather_str):
    current_weather_label = ttk.Label(text= weather_str)
    current_weather_label.place(x=62, y= 80)