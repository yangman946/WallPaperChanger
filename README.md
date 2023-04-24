

<h1 align="center">
    WallPaperChanger 🖼️
</h1>
<hr>
<p align="center">
    <img src="https://img.shields.io/badge/os-linux%2C%20windows%2C%20macos-blue.svg"> 
    <img src="https://img.shields.io/github/stars/yangman946/WallPaperChanger?color=ccf">
    <img src="https://img.shields.io/badge/license-MIT-dfd.svg">
    <img src="https://img.shields.io/github/contributors/yangman946/WallPaperChanger?color=9ea">
    
</p>

<p align="center">
    <img src="https://github.com/yangman946/WallPaperChanger/blob/main/generated/wallpaper.jpeg" alt="wallpaper">
</p>

<br>

## Description ⛈️
WallPaperChanger is a Python script that changes your desktop wallpaper according to your current time and weather.
<br>

### Features 

<ul>
  <li>Images API - new and unique wallpaper every time </li>
  <li>Weather API - changes wallpaper depending on weather (rain/mist/clear/thunder) and time (sunrise/day/sunset/night) </li>
  <li>Weather widget - Shows weather forecast </li>
  <li>Displayed time and date + refreshable clock </li>
</ul>
<br>


## Cloning 🌀

`$ git clone https://github.com/yangman946/WallPaperChanger`
<br>

## Running ⚡

You need:

- to install requirements: `pip install -r requirements.txt`
- Your own api key from openweather: https://openweathermap.org/api
- (Optional) Image url for a weather widget: customise your own widget here: https://www.theweather.com/

<i>Alternatively you can choose to run WallPaperChanger offline with a selection of default wallpapers.</i>

Refer to `settings.py` for where to insert these values. 

<br>

You can run this script in two ways:

### Via the `run.bat` batch script

You can either run the script manually or via a task scheduler to run it periodically (i.e., every hour).
Make sure to edit the `run.bat` script to add the directory for which the batch script is located.
A premade windows task scheduler xml file is provided in the project root.

You may also decide to run the `refresh.bat` script every minute to update the live clock. 

### Via the command-line

- Open the project in your terminal of choice (or use `cd` to move to the project root)
- Run the app using the following command.

  ```bash
  python -m wallpaperChanger
  ```

<br>

## Miscellaneous 🧑‍💻

### Batch files

Various batch files have been included with this project:

<ul>
  <li><code>run.bat</code> - changes the wallpaper, can be run from a task scheduler </li>
  <li><code>refresh.bat</code> - only changes the clock at the bottom right of the wallpaper </li>
  <li><code>dislike.bat</code> - can add the wallpaper to <code>blacklisted_wallpapers.txt</code>, effectively removing it from ever being seen </li>
</ul>

You can create desktop shortcuts to these batch files for quick and easy access. 




### Offline Only

You will find separate folders for each weather condition (day/night). 
These folders contain jpeg images (3936x2624 pixels) each labeled from 1 to the number of images in the folder. 
If you wish to replace images, ensure that:
<br>
<ul>
  <li>The images are of correct size (recommended 3936x2624 pixels)</li>
  <li>The images are in the correct folders</li>
  <li>The images are properly labelled {weather state}_{day state}_{image index} </li>
  <li>The images are jpeg images </li>
</ul>


### Customising layouts

To customise the layout of the wallpaper, refer to the `configurations` dictionary at `mainScript.py`.
Here, you can add custom layouts or use existing ones. Each layout requires six parameters:

<ol>
  <li>Coordinates of your widget (x, y)</li>
  <li>Day/date text location ("x", "y")</li>
    <ul>
        <li>"x": left, center or right </li>
        <li>"y": top, center or bottom </li>
    </ul>
  <li>show water mark (true, false)</li>
  <li>show compile time (true, false)</li>
  <li>Compile time location ("x", "y")</li>
    <ul>
        <li>"x": left, center or right </li>
        <li>"y": top, center or bottom </li>
    </ul>
  <li>Font</li>
    <ul>
        <li>Bold</li>
        <li>ExtraBold</li>
        <li>ExtraLight</li>
        <li>Italic</li>
        <li>Light</li>
        <li>Medium</li>
        <li>Regular</li>
        <li>Thin</li>
        <li>See all <a href = "https://github.com/yangman946/WallPaperChanger/tree/main/assets/fonts/Montserrat">fonts</a></li>
    </ul>
</ol>
<br>

## Contributing ❤️

If you wish to contribute to this project, send a pull request, and I will review it ASAP. Here’s an easy and quick [video guide](https://youtu.be/waEb2c9NDL8) for learning how to contribute via GitHub.


