import random
from pathlib import Path
from typing import List

from pywal import wallpaper
#import ctypes # test
import requests
import shutil
from . import settings


def set_wallpaper(file: Path):
    """Change wallpaper to the provided file

    :raises FileNotFoundError: if the provided file does not exist
    """
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f"'{file}' was not found.")


    wallpaper.change(str(file))
    #ctypes.windll.user32.SystemParametersInfoW(20, 0, str(file), 3) #DEBUG



def get_wallpaper_images(time_of_day: str, weather_condition: str) -> List[Path]:
    """Returns paths of all wallpapers for the select conditions"""
    return [
        p for p in
        settings.ASSETS_DIR.glob(f'./wallpapers/{time_of_day}/{weather_condition}/*')
        if p.is_file()
    ]


def get_random_wallpaper_image(time_of_day: str, weather_condition: str) -> Path:
    """Return a path pointing to random wallpaper pertaining to the conditions"""
    url = ""
    if (random.randint(0,1) == 0): # 50% chance
        try: # get api
            url = f"https://source.unsplash.com/random/3936x2624?{time_of_day}%20{weather_condition}"
            r = requests.get(url, allow_redirects=True, stream=True)

            with open(settings.DOWNLOAD, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            url = settings.DOWNLOAD
        except:
            url = random.choice(get_wallpaper_images(time_of_day, weather_condition))
    else:  
        url = random.choice(get_wallpaper_images(time_of_day, weather_condition))
        
    return url
