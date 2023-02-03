from modelo import read_user_cli_args
from modelo import build_weather_query, get_url_icon
from modelo import get_weather_json, get_weather_data, build_weather_data_set
import modelo_db
from vista import _select_weather_display_params, display_weather_info
from vista_tk import get_city_entry, flat_weather_dict, display_on_windows, vista_principal
from tkinter import Tk


if __name__ == "__main__":
    try:
        modelo_db.make_connection()
        modelo_db.create_table()
    except:
        print ("hay un error en el inicio de la db.")

    #user_args = read_user_cli_args()
    #query_url = build_weather_query(user_args.city, user_args.imperial)

    root_tk = Tk()
    vista_principal(root_tk)

    city = get_city_entry()
    query_url = build_weather_query(city)
    weather_json = get_weather_json(query_url)
    weather_data = get_weather_data(weather_json)
    weather_str = flat_weather_dict(weather_data)
    display_on_windows(weather_str)

    data_db = (weather_data["current_time"], weather_data["location"],weather_data["temperature"], weather_data["wind_speed"])
    modelo_db.insert_data(data_db)
    modelo_db.request_data_table()

    weather_data_display = build_weather_data_set(weather_data)
    #wind_desc = display_weather_info(weather_data_display, user_args.imperial)


