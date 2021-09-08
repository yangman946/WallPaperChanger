import platform
from pathlib import Path

from wallpaperChanger.exceptions import PlatformNotSupportedException

system = platform.system()  # https://docs.python.org/3/library/platform.html#platform.system

# Used to identify is a system has support to change wallpaper
# alternative to calling a method and catching the exception
system_supported = True

if system == 'Windows':
    import ctypes


    def set_wallpaper(file: Path):
        """Change windows wallpaper to the provided file

        :raises FileNotFoundError: if the provided file does not exist
        """
        if not file.exists() or not file.is_file():
            raise FileNotFoundError(f"'{file}' was not found.")

        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(file), 0)

elif system == 'Linux':
    pass

else:
    system_supported = False


    def set_wallpaper(file: Path):
        """Dummy method that throws a PlatformNotSupportedException when called"""
        raise PlatformNotSupportedException(f"'{system}' does not currently have support to change wallpaper.")
