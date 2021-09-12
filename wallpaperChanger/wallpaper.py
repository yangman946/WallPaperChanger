import random
from pathlib import Path
from typing import List

from pywal import wallpaper

from . import settings


def set_wallpaper(file: Path):
    """Change wallpaper to the provided file

    :raises FileNotFoundError: if the provided file does not exist
    """
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f"'{file}' was not found.")
    
    wallpaper.change(str(file))



def get_wallpaper_images(time_of_day: str, weather_condition: str) -> List[Path]:
    """Returns paths of all wallpapers for the select conditions"""
    return [
        p for p in
        settings.ASSETS_DIR.glob(f'./wallpapers/{time_of_day}/{weather_condition}/*')
        if p.is_file()
    ]


def get_random_wallpaper_image(time_of_day: str, weather_condition: str) -> Path:
    """Return a path pointing to random wallpaper pertaining to the conditions"""
    return random.choice(get_wallpaper_images(time_of_day, weather_condition))
