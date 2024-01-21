# ezpylogger
Highly customizable and yet very simple key logger written in python, for Windows.

After being executed, this script can seamlessy log user actions and store them either in a folder or next to the script, depending on its configuration.

As of this version, it can:
- Log key presses & mouse clicks
- Take screenshots
- Scrape browser history (chrome & edge)

## Installation
You can download the script as an executable file, compiled with pyinstaller, so that it can also be executed on machines that don't have python installed.

If you want to compile it yourself, you can just install the dependencies with pip and then compile it using pyinstaller.

```shell
pyinstaller -F ezpylogger.py
```

## Usage
You can customize this script by including a "config.json" file in the working directory (the directory from where you start up the script).

You might wanna check the ["config.json" example](config-example.json) file and its [commented version](config-explained.json5) in the repo, to get an idea of what the script can do.

By default only the keylogger will be enabled, with minimal configuration.

You can stop the script by pressing the "F12" key by default, or by killing its process (duh).


## Disclaimer
This script is for educational purposes only. I am not responsible for any damage caused by this script. Please use it responsibly.