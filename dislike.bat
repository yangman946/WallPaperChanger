@echo off

@REM add the current wallpaper to blacklisted wallpapers 
type C:\Users\Clarence\Documents\WallPaperChanger-main\debug\current_wallpaper.txt >> C:\Users\Clarence\Documents\WallPaperChanger-main\debug\blacklisted_wallpapers.txt
@REM refresh wallpapers
cd C:\Users\Clarence\Documents\WallPaperChanger-main

@REM pythonw or python-window-mode doesnt show the console
start /MIN pythonw -m wallpaperChanger none