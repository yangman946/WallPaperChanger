import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
GENERATED_DIR = BASE_DIR / 'generated'

OK_WALLPAPER = GENERATED_DIR / 'wallpaper.jpeg'
ERROR_WALLPAPER = GENERATED_DIR / 'error.jpeg'

load_dotenv()  # load environment variables.

API_KEY = os.getenv("API_KEY", '')  # place openweather api key here <------ from https://openweathermap.org/api
CITY = os.getenv("city", '')  # write your city name here in lowercase
