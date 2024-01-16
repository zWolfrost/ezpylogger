# ezpylogger
 
A really simple key logger written in python.

## Installation

You can download the script as an executable file, compiled with pyinstaller, so that it can be executed on any windows machine without having python installed.

If you want to compile it yourself, you can just install the dependencies with pip and then compile it with pyinstaller.

```bash
pyinstaller -F ezpylogger.py
```

## Usage

After being executed, this script will log all the keys pressed by the user and store them in a "keylog.txt" file located in the working directory (oftentimes the directory where the script is located).

You can stop the script by pressing the "F12" key by default, or by killing its process (duh).

## Disclaimer

This script is for educational purposes only. I am not responsible for any damage caused by this script. Please use it responsibly.