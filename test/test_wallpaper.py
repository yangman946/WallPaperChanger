import unittest

from wallpaperChanger import wallpaper


class TestWallpaper(unittest.TestCase):

    def test_get_wallpapers(self):
        wallpapers = wallpaper.get_wallpaper_images('day', 'rain')
        self.assertEqual(2, len(wallpapers))

        wallpapers = wallpaper.get_wallpaper_images('night', 'clear')
        self.assertEqual(12, len(wallpapers))
