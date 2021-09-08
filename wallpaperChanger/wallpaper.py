import platform
import subprocess
from functools import wraps
from pathlib import Path
from typing import Callable

from wallpaperChanger.exceptions import PlatformNotSupportedException

system = platform.system()  # https://docs.python.org/3/library/platform.html#platform.system

# Used to identify is a system has support to change wallpaper
# alternative to calling a method and catching the exception
system_supported = True


def _ensure_exists(func: Callable[[Path], None]):
    """Decorator that ensures that the file in the argument exists"""

    @wraps(func)
    def wrapper(file: Path):
        if not file.exists() or not file.is_file():
            raise FileNotFoundError(f"'{file}' was not found.")

        return func(file)

    return wrapper


if system == 'Windows':
    import ctypes

    @_ensure_exists
    def set_wallpaper(file: Path):
        """Change windows wallpaper to the provided file

        :raises FileNotFoundError: if the provided file does not exist
        """
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(file), 0)

elif system == 'Linux':

    # TODO add support for kde desktops
    @_ensure_exists
    def set_wallpaper(file: Path):
        """Change linux wallpaper to the provided file

        :raises FileNotFoundError: if the provided file does not exist
        """
        subprocess.Popen(
            f"gsettings set org.gnome.desktop.background picture-uri 'file://{file}'",
            shell=True,
        )

else:
    system_supported = False


    def set_wallpaper(file: Path):
        """Placeholder function that throws a PlatformNotSupportedException when called"""
        raise PlatformNotSupportedException(f"'{system}' does not currently have support to change wallpaper.")
