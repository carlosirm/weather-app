# py



PADDING = 20

REVERSE = "\033[;7m"
RESET = "\033[0m"

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"

THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)

def change_color(color):
    print(color, end="")

def _select_weather_display_params(weather_id):
    #print (str(weather_id) + "weather ID")
    if weather_id in THUNDERSTORM:
        display_params = ("💥", RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", RESET)
    return display_params

def display_weather_info (data_dic:dict, imperial=False):
    """Prints formatted weather information about a city.

    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether or not to use imperial units for temperature

    More information at https://openweathermap.org/current#name
    """
    #for clave, valor in data_dic.items():
    #    print (f"{clave} {valor}")

    change_color(REVERSE)
    print(f"{data_dic['location']:^{PADDING}}", end="")
    change_color(RESET)
    weather_symbol, color = _select_weather_display_params(data_dic['weather_id'])
    local_time = data_dic['current_local_time'].strftime("%A, %B %d, %Y")
    
    
    #print (type(data_dic['current_local_time']))
    print(f"{local_time:^{PADDING}}")
    change_color(color)
    print(f"Temperatura: ({data_dic['temperature']}°{'F' if imperial else 'C'})",end=" " )
    print(f"Sensación Termica: ({data_dic['feels_like']}°{'F' if imperial else 'C'})")
    change_color(RESET)
    print(f"{weather_symbol}", end=" ")
    print(f"{data_dic['wind_info'][0]}  {data_dic['wind_info'][1]}")



   




