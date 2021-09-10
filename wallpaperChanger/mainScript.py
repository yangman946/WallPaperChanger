"""
daily wallpaper generator: by clarence yang 4/09/20
creates a wallpaper depending on the weather!

image url for weather: customise your own here:
https://www.theweather.com/

you'll need your own api key for openweather:
https://openweathermap.org/api

You can run this script using a batch file and run it periodically (e.g., every hour) through windows task scheduler.
Make sure you edit the run.bat file to include the file location of the batch script. 
"""

# imports
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.request import urlopen, Request

import requests
from PIL import Image, ImageFont, ImageDraw

from wallpaperChanger import wallpaper
from wallpaperChanger.settings import ASSETS_DIR, GENERATED_DIR, OK_WALLPAPER, ERROR_WALLPAPER, API_KEY, CITY

from datetime import datetime
from dateutil import tz

# Step 1: get your custom weather widget from https://www.theweather.com/, 
# change the syles to your likings, Recommened transparent background and white foreground
pic_url = "https://www.theweather.com/wimages/foto9a654be7aab09bde5e0fd21539da5f0e.png"  # place custom weather url here

# Step 2: get your api key from openweather: https://openweathermap.org/api
CurrentUrl = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&mode=xml&units=metric&APPID={API_KEY}"  # <--- change parameters from settings.py

# Step 3 (optional): choose your styles/themes (see README.md)
# widget location / date text location (x, y) / water mark show / load time show / load time location / font style (see fonts)
currentTheme = "default"
configurations = {
    "default": [(3350, 200), ["center", "center"], True, True, ["right", "top"], "light"],
    "middle-left": [(3350, 200), ["left", "center"], True, True, ["right", "top"], "light"],
    "middle-right": [(3350, 200), ["right", "center"], True, True, ["right", "top"], "light"],
    "custom": [(3350, 200), ["left", "bottom"], True, True, ["right", "top"], "Medium"], # change this one to your needs, or define more themes
}

date_text_anchors = { # anchor factors
    "top": [6, 5.6], # y
    "bottom": [1.4, 1.4], # y
    "center": [2, 2], # x or y
    "right": [1.07, 1.055], # x
    "left": [12, 12], # x
}

# load fonts
font = ImageFont.truetype(str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 120)
font2 = ImageFont.truetype(str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 50)
font3 = ImageFont.truetype(str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 70)
font4 = ImageFont.truetype(str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 30)

# weather data: work on this <-- add temperature functions
City = ""
# temp = [] #current, min, max 
# clouds = ""
# weather = ""
weather_ID = 0

# image brightness
brightness = 0.4


def main():  # main function
    # get api: get wallpaper, edit texts
    global brightness, weather_ID
    try:

        # getting our weather data
        sunrise = 6
        sunset = 18
        response = requests.get(CurrentUrl)  # first get current weather
        with (GENERATED_DIR / 'feed.xml').open('wb') as file:
            file.write(
                response.content)  # write weather data to feed.xml <-- this will be automatically created if it doesnt exist.
        tree = ET.parse(GENERATED_DIR / 'feed.xml')
        root = tree.getroot()
        for child in root:

            if child.tag == "weather":
                weather_ID = child.attrib[
                    'number']  # weather ID, the weather condition is stored in a unique ID:
                # https://openweathermap.org/weather-conditions

            if child.tag == "city":  # get sunrise and sunset times
                for item in child:
                    if item.tag == "sun":
                        sunrise = datetime.strptime(item.attrib['rise'], '%Y-%m-%dT%H:%M:%S')
                        sunset = datetime.strptime(item.attrib['set'], '%Y-%m-%dT%H:%M:%S')

        # getting time
        hour = getHour()

        # sunrise and sunset are in utc
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        sunrise = sunrise.replace(tzinfo=from_zone)
        sunset = sunset.replace(tzinfo=from_zone)
        sunrise = sunrise.astimezone(to_zone)
        sunset = sunset.astimezone(to_zone)

        if hour < sunrise.hour or hour > sunset.hour:  # change this to find a sun rise sun set api
            # night
            dayState = "night"
            brightness = 0.4
            print("is day: false: {}".format(sunrise))
        else:
            brightness = 0.7
            dayState = "day"
            print("is day: true")

        weather_code = ""  # current weather
        # checking the type of weather: obviously you could go deeper and have more images,
        # see: https://openweathermap.org/weather-conditions for modifications add other weather codes if you want.
        print(weather_ID)
        if 300 <= int(weather_ID) < 623:
            # rain or snow, idk, just put it as rain
            weather_code = "rain"
        elif 700 < int(weather_ID) < 782:
            # fog or atmosphere
            weather_code = "mist"
        elif int(weather_ID) >= 800:
            weather_code = "clear"
            # clear
        elif 200 <= int(weather_ID) <= 232:
            # thunder
            weather_code = "thunder"

        createWallpaper(dayState, weather_code)  # create the wallpaper
    except requests.ConnectionError:
        # inform them of the specific error here (based off the error code)
        getFailed()
    except Exception as e:
        print(e)
        getFailed()


# failed, see which type of fail it is
def getFailed():
    try:
        img = Image.open(ERROR_WALLPAPER)
        img = img.point(lambda p: p * brightness)  # set brightness of the error wallpaper. 
        draw = ImageDraw.Draw(img)
        now = datetime.now()

        W, H = img.size

        # positioning date time text
        w, h = draw.textsize(now.strftime("%A"), font=font)
        draw.text(((W - w) / 2, (H - h) / 2), now.strftime("%A"), (255, 255, 255),
                  font=font)  # day text: what day it is

        w, h = draw.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)

        draw.text(((W - w) / 2, (H - h) / 2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year),
                  (255, 255, 255), font=font2)  # date text: the date

        # Bottom right.
        draw.text((3200, 2000), "Smart Wallpaper", (255, 255, 255), font=font3)
        draw.text((3280, 2100), "by Clarence Yang", (255, 255, 255), font=font2)
        img.save(ERROR_WALLPAPER)
    except Exception as e:  # the above code failed: perhaps the error.jpeg doesn't exist.
        print(e)  # debug
        w, h = 3936, 2424
        img = Image.new("RGB", (w, h))
        now = datetime.now()
        img1 = ImageDraw.Draw(img)
        img1.rectangle([(0, 0), img.size], fill=(102, 102, 102))  # draw the background as a plain colour

        W, H = img.size

        # positioning date time text
        w, h = img1.textsize(now.strftime("%A"), font=font)
        img1.text(((W - w) / 2, (H - h) / 2), now.strftime("%A"), (255, 255, 255), font=font)

        w, h = img1.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)

        img1.text(((W - w) / 2, (H - h) / 2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year),
                  (255, 255, 255), font=font2)  # date text

        # bottom right
        img1.text((3200, 2000), "Smart Wallpaper", (255, 255, 255), font=font3)
        img1.text((3280, 2100), "by Clarence Yang", (255, 255, 255), font=font2)
        img.save(ERROR_WALLPAPER)

    wallpaper.set_wallpaper(ERROR_WALLPAPER)


# returns current hour
def getHour():
    return datetime.now().hour


def createWallpaper(daystate, WeatherCode):  # creates wallpaper: clean code?
    print(WeatherCode)
    # if it is day
    chosen_image = wallpaper.get_random_wallpaper_image(daystate, WeatherCode)
    img = Image.open(chosen_image)  # open image
    img = img.point(lambda
                    p: p * brightness)  # change image brightness, we don't want the brightness of the background
    # to cancel out the white text.

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    im1 = Image.open(urlopen(Request(url=pic_url, headers=headers)))  # get the weather widget 

    #select layout

    # resizing and positioning the weather widget
    baseheight = 600
    hpercent = (baseheight / float(im1.size[1]))
    wsize = int((float(im1.size[0]) * float(hpercent)))
    im1 = im1.resize((wsize, baseheight))
    img.paste(im1, (configurations[currentTheme][0]), im1) # widget location

    # get current date and time. 
    draw = ImageDraw.Draw(img)
    now = datetime.now()

    # draw the day and date
    W, H = img.size
    w, h = draw.textsize(now.strftime("%A"), font=font)
    draw.text(((W - w) / date_text_anchors[configurations[currentTheme][1][0]][0], (H - h) / date_text_anchors[configurations[currentTheme][1][1]][0]), 
            now.strftime("%A"), (255, 255, 255), font=font)  # draw the day text

    # draw the date: month day year 
    w, h = draw.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)
    draw.text(((W - w) / date_text_anchors[configurations[currentTheme][1][0]][1], (H - h) / date_text_anchors[configurations[currentTheme][1][1]][1] + 100), 
            now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255, 255, 255), font=font2)

    if (configurations[currentTheme][2]):
        # bottom left add signature: you can change this if you want
        draw.text((3300, 2000), "Smart Wallpaper", (255, 255, 255),font=font2)  
        draw.text((3300, 2060), "by Clarence Yang", (255, 255, 255), font=font4)

    if (configurations[currentTheme][3]):
        # the compile time text
        w, h = draw.textsize("Updated: {}".format(now.strftime("%Y-%m-%d %H:%M:%S")), font=font4)
        draw.text(((W - w) / date_text_anchors[configurations[currentTheme][4][0]][0] + 40, (H - h) / date_text_anchors[configurations[currentTheme][4][1]][0] + 450), 
                "Updated: {}".format(now.strftime("%Y-%m-%d %H:%M:%S")), (255, 255, 255), font=font4)  # draw the day text

    # save image and set it as the current wallpaper
    img.save(OK_WALLPAPER)
    wallpaper.set_wallpaper(OK_WALLPAPER)


if __name__ == '__main__':
    # create required directories
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    main()
