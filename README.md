# ezpylogger
Highly customizable and yet very simple key logger written in python, for Windows.

After being executed, this script can seamlessy log user actions, (key presses and mouse clicks) as well as:

- Take screenshots
- Scrape browser history (chrome & edge only)
- Send emails

## Installation
You can download the script as an executable file, compiled with pyinstaller, so that it can also be executed on machines that don't have python installed.

## Building
Alternatively to the "download" option, you can install the necessary libraries with `pip install -r requirements.txt` (as well as pyinstaller) and then build the script yourself by using the "build.bat" file.

Before building, i recommend populating the "entropy" property in the "[config-default.json](src/config-default.json)" file to completely change the final pyinstaller's executable hash.

## Usage
**This script will do nothing if ran without a "config.json" file in its working directory!**

The "config.json" file will tell the script what loggers to enable and a fair number of other options.

You might wanna check out the ["config.json" example](config-example.json) file to have a starting point as well as its [commented version](config-explained.json5), to get an idea of what the script can do.

Also, the file should be ran in its working directory (double clicking it will also do), otherwise it will most likely not work properly.

## Disclaimer
This script is for educational purposes only. I am not responsible for any damage caused by this script. Please use it responsibly.