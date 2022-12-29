# weather.py

import json
import sys
from urllib import error, request
from datetime import datetime, timedelta, timezone
import json




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
    
    city = weather_json["name"]
    country = weather_json["sys"]["country"]
    location = f"{city}, {country}"
    
    weather_id = weather_json["weather"][0]["id"]
    weather_description = weather_json["weather"][0]["description"]
    weather_icon = weather_json["weather"][0]["icon"]
    temperature = weather_json["main"]["temp"]
    feels_like = weather_json["main"]["feels_like"]
    wind_speed = weather_json["wind"]["speed"]

    wind_json = open_wind_class_data ('classification_wind.json')
    wind_info = wind_classifier(wind_speed, wind_json)
    
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
                "wind_info":wind_info,
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