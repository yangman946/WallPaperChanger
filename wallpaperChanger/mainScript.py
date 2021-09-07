''' 
daily wallpaper generator: by clarence yang 4/09/20
creates a wallpaper depending on the weather!

image url for weather: customise your own here: 
https://www.theweather.com/

you'll need your own api key for openweather:
https://openweathermap.org/api 

You can run this script using a batch file and run it periodically (e.g., every hour) through windows task scheduler. 

'''

#imports
import ctypes
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import os
from urllib.request import urlopen, Request
import random
from dotenv import load_dotenv

load_dotenv() #load environment variables.

pic_url = "https://www.theweather.com/wimages/foto9a654be7aab09bde5e0fd21539da5f0e.png" #place custom weather widget URL here <------- from https://www.theweather.com/ 

current_path = os.path.dirname(os.path.realpath(__file__))
APIKEYOWM = os.getenv("API_KEY") #place openweather api key here <------ from https://openweathermap.org/api 


CurrentUrl = "http://api.openweathermap.org/data/2.5/weather?q="+os.getenv("city")+"&mode=xml&units=metric&APPID=" + APIKEYOWM # <--- replace current url (change parameters to your needs)

#load fonts
font = ImageFont.truetype(current_path + "\\Montserrat\\Montserrat-Thin.ttf", 120)
font2 = ImageFont.truetype(current_path + "\\Montserrat\\Montserrat-Thin.ttf", 50)
font3 = ImageFont.truetype(current_path + "\\Montserrat\\Montserrat-Thin.ttf", 70)


#weather data
City = ""
temp = [] #current, min, max 
clouds = ""
weather = ""
weatherID = 0

#image brightness
brightness = 0.4

def main(): #main function
    # get api: get wallpaper, edit texts
    global brightness
    try:
        
        #getting our weather data
        response = requests.get(CurrentUrl) #first get current weather
        with open(current_path + '\\feed.xml', 'wb' ) as file:
            file.write(response.content) #write weather data to feed.xml <-- this will be automatically created if it doesnt exist.
        tree = ET.parse(current_path + '\\feed.xml')
        root = tree.getroot()
        for child in root:

            if child.tag == "weather":
                weatherID = child.attrib['number'] #weather ID, the weather condition is stored in a unique ID: https://openweathermap.org/weather-conditions 
               
        
        #getting time 
        hour = getHour()

        isday = False
        if hour < 6 or hour > 18:
            #night
            isday = False
            brightness = 0.4
            print("is day: false")
            
        else:
            brightness = 0.7
            isday = True
            print("is day: true")
        
        weathercode = 0 #our custom code: 
        #checking the type of weather: obviously you could go deeper and have more images, see: https://openweathermap.org/weather-conditions for modifications
        #add other weather codes if you want.
        print(weatherID)
        if int(weatherID) >= 300 and int(weatherID) < 623:
            #rain or snow, idk, just put it as rain
            weathercode = 0
        elif int(weatherID) > 700 and int(weatherID) < 782:
            #fog or atmosphere
            weathercode = 1
        elif int(weatherID) >= 800:
            weathercode = 2
            #clear
        elif int(weatherID) >= 200 and int(weatherID) <= 232:
            #thunder
            weathercode = 3 


        createWallpaper(isday, weathercode) #create the wallpaper
    except requests.ConnectionError:
        #inform them of the specific error here (based off the error code)
        getFailed()
    except Exception as e:
        print(e)
        getFailed()
        


#failed, see which type of fail it is
def getFailed():

    try:
        chosen_image = current_path + "\\wallpapers\\error.jpeg" #use the error wallpaper
        img = Image.open(chosen_image)
        img = img.point(lambda p: p * brightness) #set brightness of the error wallpaper. 
        draw = ImageDraw.Draw(img)
        now = datetime.now()

        W, H = img.size

        #positioning date time text
        w, h = draw.textsize(now.strftime("%A"), font=font)
        draw.text(((W-w)/2,(H-h)/2), now.strftime("%A"), (255,255,255), font=font) #day text: what day it is

        w, h = draw.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2) 

        draw.text(((W-w)/2,(H-h)/2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2) #date text: the date


        #Bottom right.
        draw.text((3200,2000), "Smart Wallpaper", (255,255,255), font=font3)
        draw.text((3280,2100), "by Clarence Yang", (255,255,255), font=font2)
        img.save(current_path + "\\errorWallpaper.jpeg")
    except Exception as e: #the above code failed: perhaps the error.jpeg doesn't exist.
        print(e) #debug
        w, h = 3936, 2424
        img = Image.new("RGB", (w, h)) 
        now = datetime.now()
        img1 = ImageDraw.Draw(img)   
        img1.rectangle([(0,0),img.size], fill = (102,102,102) ) #draw the background as a plain colour

        W, H = img.size

        #positioning date time text
        w, h = img1.textsize(now.strftime("%A"), font=font)
        img1.text(((W-w)/2,(H-h)/2), now.strftime("%A"), (255,255,255), font=font)

        w, h = img1.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)

        img1.text(((W-w)/2,(H-h)/2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2) #date text


        #bottom right
        img1.text((3200,2000), "Smart Wallpaper", (255,255,255), font=font3)
        img1.text((3280,2100), "by Clarence Yang", (255,255,255), font=font2)
        img.save(current_path + "\\errorWallpaper.jpeg")

    #Set failed wallpaper 
    ctypes.windll.user32.SystemParametersInfoW(20, 0, current_path + "\\errorWallpaper.jpeg" , 0)
    

#returns current hour
def getHour():
    hour = datetime.now().hour
    return hour


def createWallpaper(isDay, WeatherCode): #creates wallpaper: clean code?
    chosen_image = ""
    
    #if it is day
    if isDay:
        #find the current weather
        if WeatherCode == 0:
            #rain
            print("rain")
            #length of all files in the chosen folder. 
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\rain_day_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\rain_day_folder", name))])
            chosen_image = current_path + "\\wallpapers\\rain_day_folder\\rain_day_{}.jpeg".format(random.randint(1,length)) #get a random image from this folder
        elif WeatherCode == 1:
            #fog
            print("fog")
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\mist_day_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\mist_day_folder", name))])
            print(length)
            chosen_image = current_path + "\\wallpapers\\mist_day_folder\\mist_day_{}.jpeg".format(random.randint(1,length))
        elif WeatherCode == 2:
            #clear
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\clear_day_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\clear_day_folder", name))])
            chosen_image = current_path + "\\wallpapers\\clear_day_folder\\clear_day_{}.jpeg".format(random.randint(1,length))
            print("clear")
        elif WeatherCode == 3:
            #thunder
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\thunder_day_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\thunder_day_folder", name))])
            chosen_image = current_path + "\\wallpapers\\thunder_day_folder\\thunder_day_{}.jpeg".format(random.randint(1,length))
            print("thunder")
    else: #if night
        #find the current weather 
        if WeatherCode == 0:
            #rain
            print("rain")
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\rain_night_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\rain_night_folder", name))])
            chosen_image = current_path + "\\wallpapers\\rain_night_folder\\rain_night_{}.jpeg".format(random.randint(1,length))
        elif WeatherCode == 1:
            #fog
            print("fog")
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\mist_night_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\mist_night_folder", name))])
            chosen_image = current_path + "\\wallpapers\\mist_night_folder\\mist_night_{}.jpeg".format(random.randint(1,length))
        elif WeatherCode == 2:
            #clear
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\clear_night_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\clear_night_folder", name))])
            chosen_image = current_path + "\\wallpapers\\clear_night_folder\\clear_night_{}.jpeg".format(random.randint(1,length))
            print("clear")
        elif WeatherCode == 3:
            #thunder
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\thunder_night_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\thunder_night_folder", name))])
            chosen_image = current_path + "\\wallpapers\\thunder_night_folder\\thunder_night_{}.jpeg".format(random.randint(1,length))
            print("thunder")
    
    
    img = Image.open(chosen_image) #open image
    img = img.point(lambda p: p * brightness) #change image brightness, we don't want the brightness of the background to cancel out the white text. 

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    
    im1 = Image.open(urlopen(Request(url=pic_url, headers=headers))) #get the weather widget 

    #resizing and positioning the weather widget
    baseheight = 600
    hpercent = (baseheight / float(im1.size[1]))
    wsize = int((float(im1.size[0]) * float(hpercent)))
    im1 = im1.resize((wsize, baseheight))
    img.paste(im1, (3350,200), im1)

    #get current date and time. 
    draw = ImageDraw.Draw(img)
    now = datetime.now()

    #draw the day and date
    W, H = img.size
    w, h = draw.textsize(now.strftime("%A"), font=font) 
    draw.text(((W-w)/2,(H-h)/2), now.strftime("%A"), (255,255,255), font=font) #draw the day

    #draw the date: month day year 
    w, h = draw.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)
    draw.text(((W-w)/2,(H-h)/2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2)

    #bottom left add signature: you can change this if you want
    draw.text((3200,2000), "Smart Wallpaper", (255,255,255), font=font3) #positioning was more or less trial and error.
    draw.text((3280,2100), "by Clarence Yang", (255,255,255), font=font2)

    #save image and set it as the current wallpaper
    img.save(current_path + "\\currentWallpaper.jpeg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, current_path + "\\currentWallpaper.jpeg" , 0)

main() #run

