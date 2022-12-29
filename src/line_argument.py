import argparse


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