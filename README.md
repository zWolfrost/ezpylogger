# ezpylogger
Highly customizable and yet very simple key logger written in python, for Windows.

After being executed, this script can seamlessy log user actions and store them either in a folder or next to the script, depending on its configuration.

As of this version, it can:
- Log key presses & mouse clicks
- Take screenshots
- Scrape browser history (supports chrome & edge)
- Send emails

All the executable files are created using pyinstaller (`pyinstaller -F file.pyw`) and you can also compile them by yourself if you want to, once having installed the [requirements](requirements.txt) with `pip install -r requirements.txt`, of course.

## Installation
From v1.7.0 the releases tab will have an executable file that contains the python interpreter & all the necessary requirements to run the script, but not the actual script.

In other words, its only purpose is to **run** the script.

That means that the executable file **will not work** if it doesn't find the "ezpylogger.pyw" file in the same folder, so you'll have to download that as well.

## Usage
**This script will give an error if ran without a "config.json" file in its working directory!**

The "config.json" file will tell the script what loggers to enable and numerous other options.

You might wanna check out the (downloadable) ["config.json" example](config-example.json) file to have a starting point as well as its [commented version](config-explained.json5), to get an idea of what the script can do.

## Disclaimer
This script is for educational purposes only. I am not responsible for any damage caused by this script. Please use it responsibly.