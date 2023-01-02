from src.line_argument import read_user_cli_args
from src.api_manager import build_weather_query, get_url_icon
from src.style import _select_weather_display_params, display_weather_info
from src.weather import get_weather_json, get_weather_data


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_json = get_weather_json(query_url)
    weather_data = get_weather_data(weather_json)


    wind_desc = display_weather_info(weather_data, user_args.imperial)

