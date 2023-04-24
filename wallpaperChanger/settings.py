''' 
    Thank you for using WallPaperChanger, an open source python program that changes your wallpaper depending on the weather.
    Before you run this program, please refer to README.md. In this script, you should insert your API keys. 

    Remember, this project is open source, if you would like to contribute, please fork the github repo: https://github.com/yangman946/WallPaperChanger 
    then send a pull request. 
'''

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # load environment variables.

# Step 1: get your custom weather widget from https://www.theweather.com/, 
# change the syles to your likings, I recommened transparent background with white foreground
PIC_URL = "https://www.theweather.com/wimages/foto9a654be7aab09bde5e0fd21539da5f0e.png"  # place custom weather url here

# Step 2: get your own api key from openweather: https://openweathermap.org/api
API_KEY = os.getenv("API_KEY", '')  # place openweather api key here <------ from https://openweathermap.org/api
CITY = os.getenv("city", '')  # write your city name here in lowercase

# Step 3 (optional): choose your styles/themes (see README.md)
CURRENT_THEME = "default"

# Set this to true if you do not wish to use any APIs
OFFLINE = False 

ISWINDOWS = (os.name == 'nt')

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
GENERATED_DIR = BASE_DIR / 'generated'
DEBUG_DIR =  BASE_DIR / 'debug'

TEMPLATE = GENERATED_DIR / 'template.jpeg'
DOWNLOAD = GENERATED_DIR / 'download.jpeg'
OK_WALLPAPER = GENERATED_DIR / 'wallpaper.jpeg'
ERROR_WALLPAPER = GENERATED_DIR / 'error.jpeg'
ERROR_BG = GENERATED_DIR / 'errorpic.jpeg'


