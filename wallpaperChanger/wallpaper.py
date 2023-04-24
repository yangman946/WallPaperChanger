import random
from pathlib import Path
from typing import List
import PIL
from pywal import wallpaper
import requests
import shutil
from . import settings


def set_wallpaper(file: Path):
    """Change wallpaper to the provided file

    :raises FileNotFoundError: if the provided file does not exist
    """
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f"'{file}' was not found.")

    if settings.ISWINDOWS:
        # for some reason windows doesn't like the wallpaper module, It might just be my computer though, feel free to remove this if you're on linux or mac
        import ctypes 
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(file), 3) 
    else:
        wallpaper.change(str(file))



def get_wallpaper_images(time_of_day: str, weather_condition: str) -> List[Path]:
    """Returns paths of all wallpapers for the select conditions"""
    return [
        p for p in
        settings.ASSETS_DIR.glob(f'./wallpapers/{time_of_day}/{weather_condition}/*')
        if p.is_file()
    ]


def get_random_wallpaper_image(time_of_day, weather_condition: str) -> Path:
    """Return a path pointing to random wallpaper pertaining to the conditions"""
    

    if (settings.OFFLINE == False): 
        try: # get api
            
            ur = f"https://source.unsplash.com/random/3936x2624?{time_of_day[-1]}%20{weather_condition}"
            r = requests.get(ur, allow_redirects=True, stream=True)
            print(r.url)
            
            working = True

            while working:
                with open(f"{settings.DEBUG_DIR}\\blacklisted_wallpapers.txt") as checker:
                    if str(r.url) in checker.read():
                        r = requests.get(ur, allow_redirects=True, stream=True) # repeat search if in blacklisted
                    else:
                        working = False

            if r.status_code == 200:
                with open(settings.DOWNLOAD, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                url = settings.DOWNLOAD

            f = open(f"{settings.DEBUG_DIR}\\current_wallpaper.txt", "w")
            f.write(str(r.url))
            f.close
        except IOError:
            print("error")
            url = random.choice(get_wallpaper_images(time_of_day[0], weather_condition))
            f = open(f"{settings.DEBUG_DIR}\\current_wallpaper.txt", "w") # debug purposes
            f.write(str(url))
            f.close

        if PIL.Image.open(settings.DOWNLOAD).size[0] < 3000:
            url = random.choice(get_wallpaper_images(time_of_day[0], weather_condition))
            f = open(f"{settings.DEBUG_DIR}\\current_wallpaper.txt", "w")
            f.write(str(url))
            f.close
    else:
        url = random.choice(get_wallpaper_images(time_of_day[0], weather_condition))
        
    return url
