''' 
daily wallpaper generator: by clarence yang 4/09/20
creates a wallpaper depending on the weather!

image url for weather: customise your own here: 
https://www.theweather.com/

you'll need your own api key for openweather:
https://openweathermap.org/api 

You can run this script using a batch file and run it periodically (e.g., every hour) through windows task scheduler. 

'''

import ctypes
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import os
from urllib.request import urlopen, Request
import random
#import imgkit
from dotenv import load_dotenv

load_dotenv()

pic_url = "https://www.theweather.com/wimages/foto9a654be7aab09bde5e0fd21539da5f0e.png" #place custom weather widget URL here <------- from https://www.theweather.com/ 

current_path = os.path.dirname(os.path.realpath(__file__))
APIKEYOWM = os.getenv("API_KEY") #place openweather api key here <------ from https://openweathermap.org/api 


CurrentUrl = "http://api.openweathermap.org/data/2.5/weather?q="+os.getenv("city")+"&mode=xml&units=metric&APPID=" + APIKEYOWM # <--- replace current url (change parameters to your needs)
font = ImageFont.truetype(current_path + "\\Montserrat\\Montserrat-Thin.ttf", 120)
font2 = ImageFont.truetype(current_path + "\\Montserrat\\Montserrat-Thin.ttf", 50)
font3 = ImageFont.truetype(current_path + "\\Montserrat\\Montserrat-Thin.ttf", 70)

imgURL = ""

#data
City = ""
temp = [] #current, min, max 
clouds = ""
weather = ""
weatherID = 0

offset = 1500

brightness = 0.4

def main(): #main function
    # get api: get wallpaper, edit texts
    global brightness
    try:
        
        #getting our weather data
        response = requests.get(CurrentUrl) #first get current weather
        with open(current_path + '\\feed.xml', 'wb' ) as file:
            file.write(response.content)
        tree = ET.parse(current_path + '\\feed.xml')
        root = tree.getroot()
        for child in root:

            if child.tag == "weather":
                #weather = child.attrib['value']
                weatherID = child.attrib['number']
                #imgURL = "http://openweathermap.org/img/wn/{}@2x.png".format(child.attrib['icon'])
        
        #getting time 
        hour = getHour()
        #print(imgURL)
        isday = False
        if hour < 6 or hour > 18:
            #night
            isday = False
            brightness = 0.4
            print("is day: false")
            #ctypes.windll.user32.SystemParametersInfoW(20, 0, current_path + "\\wallpapers\\clear_night.jpg" , 0)
        else:
            brightness = 0.7
            isday = True
            print("is day: true")
        
        weathercode = 0
        #checking the type of weather: obviously you could go deeper and have more images, see: https://openweathermap.org/weather-conditions for modifications
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
        #urllib.request.urlretrieve(imgURL, "icon.jpg")
        #print(asdf) #evokes error
        
        
        #local_file = open(current_path+"\\out.png",'wb')
        #requests.get(url=pic_url, stream=True).raw
        
        #req = Request(url=pic_url, headers=headers)
        '''
        with urlopen(req) as response:
            time.sleep(1)
            local_file.write(response.read())
        '''

        createWallpaper(isday, weathercode)
    except requests.ConnectionError:
        #inform them of the specific error here (based off the error code)
        getFailed()
    except Exception as e:
        print(e)
        getFailed()
        


#failed, see which type of fail it is
def getFailed():

    try:
        chosen_image = current_path + "\\wallpapers\\error.jpeg"
        img = Image.open(chosen_image)
        img = img.point(lambda p: p * brightness)
        draw = ImageDraw.Draw(img)
        now = datetime.now()

        W, H = img.size

        w, h = draw.textsize(now.strftime("%A"), font=font)
        draw.text(((W-w)/2,(H-h)/2), now.strftime("%A"), (255,255,255), font=font)

        w, h = draw.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)

        draw.text(((W-w)/2,(H-h)/2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2)


        #draw.text((3250,350), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2)
        draw.text((3200,2000), "Smart Wallpaper", (255,255,255), font=font3)
        draw.text((3280,2100), "by Clarence Yang", (255,255,255), font=font2)
        img.save(current_path + "\\errorWallpaper.jpeg")
    except Exception as e:
        print(e)
        w, h = 3936, 2424
        img = Image.new("RGB", (w, h)) 
        now = datetime.now()
        img1 = ImageDraw.Draw(img)   
        img1.rectangle([(0,0),img.size], fill = (102,102,102) )

        W, H = img.size

        w, h = img1.textsize(now.strftime("%A"), font=font)
        img1.text(((W-w)/2,(H-h)/2), now.strftime("%A"), (255,255,255), font=font)

        w, h = img1.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)

        img1.text(((W-w)/2,(H-h)/2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2)


        img1.text((3200,2000), "Smart Wallpaper", (255,255,255), font=font3)
        img1.text((3280,2100), "by Clarence Yang", (255,255,255), font=font2)
        img.save(current_path + "\\errorWallpaper.jpeg")

    #failed wallpaper 
    ctypes.windll.user32.SystemParametersInfoW(20, 0, current_path + "\\errorWallpaper.jpeg" , 0)
    

def getHour():
    hour = datetime.now().hour
    return hour

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text) 
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''         
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word, 
            # add the line to the lines array
            lines.append(line)    
    return lines

def createWallpaper(isDay, WeatherCode):
    chosen_image = ""
    
    if isDay:
        #do something
        if WeatherCode == 0:
            #rain
            print("rain")
            length = len([name for name in os.listdir(current_path + "\\wallpapers\\rain_day_folder") if os.path.isfile(os.path.join(current_path + "\\wallpapers\\rain_day_folder", name))])
            chosen_image = current_path + "\\wallpapers\\rain_day_folder\\rain_day_{}.jpeg".format(random.randint(1,length))
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
    else:
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
    
    img = Image.open(chosen_image)
    img = img.point(lambda p: p * brightness)
    #im1 = Image.open(current_path +"\\out.png")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    
    im1 = Image.open(urlopen(Request(url=pic_url, headers=headers)))

    baseheight = 600

    hpercent = (baseheight / float(im1.size[1]))
    wsize = int((float(im1.size[0]) * float(hpercent)))
    im1 = im1.resize((wsize, baseheight))


    img.paste(im1, (3350,200), im1)
    draw = ImageDraw.Draw(img)
    now = datetime.now()
    #print(now.strftime("%A"))

    W, H = img.size
    w, h = draw.textsize(now.strftime("%A"), font=font)
    #draw.text(((3230-w)/2 + offset,(200-h)/2), now.strftime("%A"), (255,255,255), font=font) #saturday
    draw.text(((W-w)/2,(H-h)/2), now.strftime("%A"), (255,255,255), font=font)
    #print(City)

    w, h = draw.textsize(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)
    #w, h = draw.textsize(now.strftime(now.strftime("%B") + " " + str(now.day) + " " + str(now.year)))
    draw.text(((W-w)/2,(H-h)/2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year), (255,255,255), font=font2)





    #works
    draw.text((3200,2000), "Smart Wallpaper", (255,255,255), font=font3)
    draw.text((3280,2100), "by Clarence Yang", (255,255,255), font=font2)
    img.save(current_path + "\\currentWallpaper.jpeg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, current_path + "\\currentWallpaper.jpeg" , 0)

main()

